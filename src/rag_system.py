import asyncio
import hashlib
import os
import re
from typing import Dict, List, Optional

import numpy as np
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from langchain.retrievers import EnsembleRetriever
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_ollama import OllamaLLM

import config
from notion_api_interactor import fetch_all_paginated_results, make_md_from_block


class RAGSystem:
    def __init__(self):
        self.vectorstore = None
        self.qa_chains = {}
        self.bm25_retriever = None
        self._doc_image_maps: Dict[str, Dict[str, str]] = {}
        self._search_cache = {}
        self._cache_max_size = 100
        self.max_context_messages = 3
        self.max_tokens_per_context = 3000

        self.embeddings = HuggingFaceEmbeddings(
            model_name=config.EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True, "batch_size": 64},
        )

        self.llm = OllamaLLM(
            model=str(config.OLLAMA_MODEL),
            base_url=str(config.OLLAMA_BASE_URL),
            temperature=0.1,
            num_ctx=3000,
            num_predict=512,
            repeat_penalty=1.1,
            top_k=20,
            top_p=0.85,
            stop=["<|end_of_text|>", "\nВОПРОС:", "ВОПРОС:", "\nUser:", "\nHuman:"],
            num_thread=os.cpu_count() or 4,
        )

    def _generate_cache_key(self, question: str, user_id: int, history_len: int) -> str:
        return hashlib.md5(f"{user_id}:{history_len}:{question.lower().strip()}".encode()).hexdigest()

    def _get_from_cache(self, key: str) -> Optional[Dict]:
        return self._search_cache.get(key)

    def _save_to_cache(self, key: str, result: Dict):
        if len(self._search_cache) >= self._cache_max_size:
            del self._search_cache[next(iter(self._search_cache))]
        self._search_cache[key] = result

    def _resolve_images_from_sources(self, sources: List[Document]) -> List[str]:
        final_images = []
        seen_urls = set()
        for doc in sources:
            for url in doc.metadata.get("chunk_images", {}).values():
                if url not in seen_urls:
                    final_images.append(url)
                    seen_urls.add(url)
        return final_images

    async def load_notion_documents_async(self) -> List[Document]:
        config.logger.info("Loading data from Notion API")
        headers = {
            "Authorization": f"Bearer {config.NOTION_TOKEN}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }
        try:
            loop = asyncio.get_event_loop()
            all_pages = await loop.run_in_executor(
                None,
                fetch_all_paginated_results,
                "https://api.notion.com/v1/search",
                headers,
                "POST",
                {"filter": {"value": "page", "property": "object"}},
            )
            if not all_pages:
                return []

            documents = []
            self._doc_image_maps = {}

            for i, page in enumerate(all_pages):
                page_id = page["id"]
                page_url = page.get("url", "")
                page_title = "Untitled"
                for value in page.get("properties", {}).values():
                    if value["type"] == "title" and value["title"]:
                        page_title = value["title"][0]["plain_text"]
                        break

                all_blocks = await loop.run_in_executor(
                    None,
                    fetch_all_paginated_results,
                    f"https://api.notion.com/v1/blocks/{page_id}/children",
                    headers,
                    "GET",
                    None,
                )

                current_page_images_map: Dict[str, str] = {}
                full_text = "".join(make_md_from_block(b, current_page_images_map) for b in all_blocks)

                if not full_text.strip():
                    continue

                self._doc_image_maps[page_id] = current_page_images_map
                print(f"{page_title} | {len(full_text)} chars | {len(current_page_images_map)} images")

                documents.append(Document(
                    page_content=full_text,
                    metadata={
                        "title": page_title,
                        "source": page_url,
                        "doc_id": i,
                        "id": page_id,
                        "char_count": len(full_text),
                    },
                ))

            config.logger.info(f"Loaded {len(documents)} pages")
            return documents
        except Exception as e:
            config.logger.error(f"Error loading documents: {e}")
            import traceback
            config.logger.error(traceback.format_exc())
            return []

    def split_documents(self, documents: List) -> List:
        if not documents:
            return []
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
            length_function=len,
            separators=config.SEPARATORS,
            is_separator_regex=False,
        )
        try:
            chunks = text_splitter.split_documents(documents)
            for chunk in chunks:
                page_id = chunk.metadata.get("id", "")
                doc_image_map = self._doc_image_maps.get(page_id, {})
                found_ids = re.findall(r"(img_[a-f0-9]{8})", chunk.page_content)
                chunk.metadata["chunk_images"] = {
                    img_id: doc_image_map[img_id]
                    for img_id in found_ids
                    if img_id in doc_image_map
                }
            config.logger.info(f"Created {len(chunks)} chunks")
            return chunks
        except Exception as e:
            config.logger.error(f"Error splitting: {e}")
            return []

    def create_vectorstore(self, chunks: List) -> None:
        if not chunks:
            return
        self.vectorstore = FAISS.from_documents(documents=chunks, embedding=self.embeddings)
        save_path = str(config.VECTOR_DB_PATH)
        os.makedirs(save_path, exist_ok=True)
        self.vectorstore.save_local(save_path)
        self.bm25_retriever = BM25Retriever.from_documents(chunks)
        self.bm25_retriever.k = 3
        config.logger.info(f"FAISS saved: {self.vectorstore.index.ntotal} vectors")

    def load_vectorstore(self):
        if not os.path.exists(config.VECTOR_DB_PATH):
            raise FileNotFoundError("FAISS DB not found")
        self.vectorstore = FAISS.load_local(
            config.VECTOR_DB_PATH, self.embeddings, allow_dangerous_deserialization=True
        )
        docs = [
            Document(page_content=doc.page_content, metadata=doc.metadata)
            for doc in self.vectorstore.docstore._dict.values()
        ]
        if docs:
            self.bm25_retriever = BM25Retriever.from_documents(docs)
            self.bm25_retriever.k = 3
            for doc in docs:
                page_id = doc.metadata.get("id", "")
                chunk_images = doc.metadata.get("chunk_images", {})
                if page_id and chunk_images:
                    self._doc_image_maps.setdefault(page_id, {}).update(chunk_images)

    def create_qa_chain(self, user_id: int):
        if self.vectorstore is None:
            return

        condense_template = """На основе истории диалога и нового вопроса, сформулируй самодостаточный вопрос на русском языке.
Если вопрос не связан с историей — верни его без изменений.

История диалога:
{chat_history}

Новый вопрос: {question}

Самодостаточный вопрос на русском:"""

        prompt_template = """Ты — ассистент. Твой единственный источник знаний — КОНТЕКСТ ниже.

СТРОГИЕ ПРАВИЛА (нарушение недопустимо):
1. Используй ТОЛЬКО информацию из КОНТЕКСТА. Никаких знаний из обучения.
2. Если ответа нет в КОНТЕКСТЕ — выведи ровно одну строку: "Информация отсутствует в базе знаний."
3. Не дополняй, не домысливай, не расширяй ответ за пределы КОНТЕКСТА.
4. Отвечай на русском языке.

КОНТЕКСТ:
{context}

ВОПРОС: {question}

ОТВЕТ (только из контекста):"""

        memory = ConversationBufferWindowMemory(
            k=self.max_context_messages,
            memory_key="chat_history",
            return_messages=True,
            output_key="answer",
        )

        faiss_retriever = self.vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 5, "fetch_k": 15, "lambda_mult": 0.7},
        )

        if self.bm25_retriever:
            self.bm25_retriever.k = 5
            ensemble = EnsembleRetriever(
                retrievers=[self.bm25_retriever, faiss_retriever],
                weights=[0.4, 0.6],
            )
            seen_in_retriever = set()
            _k = 3

            def _dedup_invoke(query, _e=ensemble, _seen=seen_in_retriever, _k=_k):
                docs = _e.invoke(query)
                result = []
                seen = set()
                for doc in docs:
                    key = doc.page_content[:200]
                    if key not in seen:
                        seen.add(key)
                        result.append(doc)
                    if len(result) >= _k:
                        break
                return result

            from langchain_core.retrievers import BaseRetriever
            from langchain_core.callbacks import CallbackManagerForRetrieverRun

            class _DeduplicatingRetriever(BaseRetriever):
                def _get_relevant_documents(self, query: str, *, run_manager: CallbackManagerForRetrieverRun = None):
                    docs = ensemble.invoke(query)
                    result, seen = [], set()
                    for doc in docs:
                        key = doc.page_content[:200]
                        if key not in seen:
                            seen.add(key)
                            result.append(doc)
                        if len(result) >= 3:
                            break
                    return result

            retriever = _DeduplicatingRetriever()
        else:
            retriever = faiss_retriever

        self.qa_chains[user_id] = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            memory=memory,
            return_source_documents=True,
            condense_question_prompt=PromptTemplate.from_template(condense_template),
            combine_docs_chain_kwargs={"prompt": PromptTemplate(
                template=prompt_template, input_variables=["context", "question"]
            )},
            get_chat_history=lambda h: h,
            verbose=False,
            max_tokens_limit=self.max_tokens_per_context,
        )

    async def initialize(self, force_reload: bool = False) -> bool:
        config.logger.info("Initializing RAG system...")
        try:
            if force_reload or not os.path.exists(str(config.VECTOR_DB_PATH)):
                documents = await self.load_notion_documents_async()
                if not documents:
                    return False
                chunks = self.split_documents(documents)
                if not chunks:
                    return False
                self.create_vectorstore(chunks)
            else:
                self.load_vectorstore()
            config.logger.info("RAG initialized!")
            return True
        except Exception as e:
            config.logger.error(f"Initialization error: {e}")
            import traceback
            config.logger.error(traceback.format_exc())
            return False

    def query(self, question: str, user_id: int) -> Dict:
        try:
            history_len = 0
            if user_id in self.qa_chains:
                try:
                    history_len = len(self.qa_chains[user_id].memory.chat_memory.messages)
                except Exception:
                    pass

            cache_key = self._generate_cache_key(question, user_id, history_len)
            cached = self._get_from_cache(cache_key)
            if cached:
                return cached

            if user_id not in self.qa_chains:
                self.create_qa_chain(user_id)

            response = self.qa_chains[user_id].invoke({"question": question})
            answer = response.get("answer", "")
            sources = response.get("source_documents", [])

            final_images = self._resolve_images_from_sources(sources)

            clean_answer = re.sub(r"\(?img_[a-f0-9]{8}\)?", "", answer)
            clean_answer = re.sub(r"!\[.*?\]\(.*?\)", "", clean_answer).strip()

            retrieval_cosine = {"mean": 0.0, "max": 0.0, "min": 0.0, "std": 0.0}
            retrieval_diversity = 0.0
            try:
                from rag_statistics import RetrievalAnswerCorrelation
                chunk_texts = [doc.page_content for doc in sources]
                if chunk_texts:
                    chunk_embeddings = self.embeddings.embed_documents(chunk_texts)
                    query_vec = np.array(self.embeddings.embed_query(question))
                    chunk_vecs = [np.array(e) for e in chunk_embeddings]
                    retrieval_cosine = RetrievalAnswerCorrelation.chunk_query_cosine(query_vec, chunk_vecs)
                    retrieval_diversity = RetrievalAnswerCorrelation.retrieval_diversity(chunk_vecs)
            except Exception as emb_err:
                config.logger.warning(f"Embedding stats error: {emb_err}")

            result = {
                "answer": clean_answer,
                "images": final_images,
                "sources": sources,
                "retrieval_cosine": retrieval_cosine,
                "retrieval_diversity": retrieval_diversity,
            }
            self._save_to_cache(cache_key, result)
            return result

        except Exception as e:
            config.logger.error(f"Query error: {e}")
            import traceback
            config.logger.error(traceback.format_exc())
            return {"answer": "Произошла ошибка. Попробуй /clear или перефразируй вопрос.", "images": [], "sources": [], "retrieval_cosine": {}, "retrieval_diversity": 0.0}

    def clear_memory(self, user_id: int):
        if user_id in self.qa_chains:
            self.qa_chains[user_id].memory.clear()
            self._search_cache.clear()


rag_system = RAGSystem()
