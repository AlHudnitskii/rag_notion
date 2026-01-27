import asyncio
import hashlib
import os
import re
from typing import Dict, List, Optional

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
from notion_api_interactor import (extract_and_resolve_images,
                                   fetch_all_paginated_results,
                                   make_md_from_block)


class RAGSystem:
    """Optimized RAG system with caching and parallel processing"""

    def __init__(self):
        self.vectorstore = None
        self.qa_chains = {}
        self.bm25_retriever = None

        self._search_cache = {}
        self._cache_max_size = 100

        self.max_context_messages = 4
        self.max_tokens_per_context = 4096

        config.logger.info(f"Initializing embedding model: {config.EMBEDDING_MODEL}")

        self.embeddings = HuggingFaceEmbeddings(
            model_name=config.EMBEDDING_MODEL,
            model_kwargs={
                "device": "cpu",
            },
            encode_kwargs={
                "normalize_embeddings": True,
                "batch_size": 32,
            },
        )

        config.logger.info("Embedding model has been loaded")

        config.logger.info(
            f"Initializing Ollama: {config.OLLAMA_BASE_URL}, model: {config.OLLAMA_MODEL}"
        )

        self.llm = OllamaLLM(
            model=str(config.OLLAMA_MODEL),
            base_url=str(config.OLLAMA_BASE_URL),
            temperature=0.1,
            num_ctx=4096,
            num_predict=384,
            repeat_penalty=1.1,
            top_k=40,
            top_p=0.9,
            stop=["<|end_of_text|>", "\nВОПРОС:", "ВОПРОС:"],
            num_thread=4,
        )
        config.logger.info("Ollama has been initialized with optimizations")

    def _generate_cache_key(self, question: str, user_id: int) -> str:
        """Generate cache key for request."""

        cache_str = f"{user_id}:{question.lower().strip()}"
        return hashlib.md5(cache_str.encode()).hexdigest()

    def _get_from_cache(self, cache_key: str) -> Optional[Dict]:
        """Get result from cache."""

        return self._search_cache.get(cache_key)

    def _save_to_cache(self, cache_key: str, result: Dict):
        """Save result to cache."""

        if len(self._search_cache) >= self._cache_max_size:
            oldest_key = next(iter(self._search_cache))
            del self._search_cache[oldest_key]

        self._search_cache[cache_key] = result

    async def load_notion_documents_async(self) -> List[Document]:
        """Async loading of documents from Notion API"""

        config.logger.info("Loading data from Notion API (async)")

        headers = {
            "Authorization": f"Bearer {config.NOTION_TOKEN}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }
        search_params = {"filter": {"value": "page", "property": "object"}}
        search_url = "https://api.notion.com/v1/search"

        try:
            loop = asyncio.get_event_loop()
            all_pages = await loop.run_in_executor(
                None,
                fetch_all_paginated_results,
                search_url,
                headers,
                "POST",
                search_params,
            )

            if not all_pages:
                config.logger.warning("No pages found.")
                return []

            config.logger.info(f"Found {len(all_pages)} pages. Processing...")

            documents = []
            for i, page in enumerate(all_pages):
                page_id = page["id"]
                page_url = page.get("url", "")
                page_title = "Untitled"
                props = page.get("properties", {})

                for key, value in props.items():
                    if value["type"] == "title" and value["title"]:
                        page_title = value["title"][0]["plain_text"]
                        break

                blocks_url = f"https://api.notion.com/v1/blocks/{page_id}/children"

                all_blocks = await loop.run_in_executor(
                    None, fetch_all_paginated_results, blocks_url, headers, "GET", None
                )

                text_parts = []

                current_page_images_map = {}

                for block in all_blocks:
                    text_chunk = make_md_from_block(block, current_page_images_map)
                    text_parts.append(text_chunk)

                full_text = "".join(text_parts)

                if not full_text.strip():
                    continue

                img_count = len(current_page_images_map)
                print(
                    f"✅ Loaded: '{page_title}' | Лен: {len(full_text)} | Картинки: {img_count}"
                )

                doc = Document(
                    page_content=full_text,
                    metadata={
                        "title": page_title,
                        "source": page_url,
                        "doc_id": i,
                        "id": page_id,
                        "char_count": len(full_text),
                        "image_map": current_page_images_map,
                    },
                )
                documents.append(doc)

            config.logger.info(
                f"Statistics: {len(documents)} source pages loaded (before splitting)"
            )
            return documents

        except Exception as e:
            config.logger.error(f"Error loading documents: {e}")
            import traceback

            config.logger.error(traceback.format_exc())
            return []

    def split_documents(self, documents: List) -> List:
        """Optimized document splitting."""

        if not documents:
            return []

        config.logger.info(f"Splitting {len(documents)} documents...")

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
            length_function=lambda text: len(text.split()),
            separators=config.SEPARATORS,
            is_separator_regex=False,
        )

        try:
            chunks = text_splitter.split_documents(documents)
            config.logger.info(f"Created {len(chunks)} chunks")
            return chunks

        except Exception as e:
            config.logger.error(f"Error splitting: {e}")
            return []

    def create_vectorstore(self, chunks: List) -> None:
        """Create vectorstore."""

        if not chunks:
            return

        config.logger.info(f"Creating FAISS vectorstore with {len(chunks)} chunks...")

        try:
            self.vectorstore = FAISS.from_documents(
                documents=chunks,
                embedding=self.embeddings,
            )

            save_path = str(config.VECTOR_DB_PATH)
            os.makedirs(save_path, exist_ok=True)
            self.vectorstore.save_local(save_path)

            self.bm25_retriever = BM25Retriever.from_documents(chunks)
            self.bm25_retriever.k = 5

            config.logger.info(
                f"FAISS index saved: {self.vectorstore.index.ntotal} vectors"
            )

        except Exception as e:
            config.logger.error(f"Error creating vectorstore: {e}")
            raise

    def load_vectorstore(self):
        if not os.path.exists(config.VECTOR_DB_PATH):
            raise FileNotFoundError("FAISS DB not found")

        self.vectorstore = FAISS.load_local(
            config.VECTOR_DB_PATH, self.embeddings, allow_dangerous_deserialization=True
        )

        try:
            docs = []
            for doc_id, doc in self.vectorstore.docstore._dict.items():
                docs.append(
                    Document(page_content=doc.page_content, metadata=doc.metadata)
                )

            if docs:
                self.bm25_retriever = BM25Retriever.from_documents(docs)
                self.bm25_retriever.k = 5
                config.logger.info(f"BM25 restored with {len(docs)} docs")
            else:
                config.logger.warning("Vectorstore is empty inside! Cannot init BM25.")
        except Exception as e:
            config.logger.error(f"Error restoring BM25: {e}")

    def create_qa_chain(self, user_id: int):
        """Create QA chain"""
        if self.vectorstore is None:
            config.logger.error("Cannot create QA chain: vectorstore is None")
            return

        try:
            condense_template = """История: {chat_history}
Вопрос: {question}
Перефразируй на русском:"""

            CONDENSE_PROMPT = PromptTemplate.from_template(condense_template)

            prompt_template = """Ты - ассистент. Твоя задача - отвечать ИСКЛЮЧИТЕЛЬНО на основе контекста.
        
ИНСТРУКЦИЯ ПО ИЗОБРАЖЕНИЯМ:
1. В тексте могут быть метки (img_xxxxxxxx) - это коды картинок.
2. Если в контексте НЕТ таких меток, НЕ ПИШИ никаких ID (вроде img123456).
3. Если метка есть и подходит по смыслу - напиши её в конце ответа.

КОНТЕКСТ:
{context}

ВОПРОС: {question}
ОТВЕТ (на русском):"""

            PROMPT = PromptTemplate(
                template=prompt_template, input_variables=["context", "question"]
            )

            memory = ConversationBufferWindowMemory(
                k=self.max_context_messages,
                memory_key="chat_history",
                return_messages=True,
                output_key="answer",
            )

            faiss_retriever = self.vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={
                    "k": 4,
                },
            )

            if self.bm25_retriever:
                ensemble_retriever = EnsembleRetriever(
                    retrievers=[self.bm25_retriever, faiss_retriever],
                    weights=[0.4, 0.6],
                )
                retriever = ensemble_retriever
                config.logger.info("Using Ensemble Retriever (Hybrid)")
            else:
                retriever = faiss_retriever
                config.logger.info("Using FAISS Retriever (Vector only)")

            qa_chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=retriever,
                memory=memory,
                return_source_documents=True,
                condense_question_prompt=CONDENSE_PROMPT,
                combine_docs_chain_kwargs={"prompt": PROMPT},
                get_chat_history=lambda h: h,
                verbose=False,
                max_tokens_limit=self.max_tokens_per_context,
            )

            self.qa_chains[user_id] = qa_chain
            config.logger.info(f"QA цепочка успешно создана для пользователя {user_id}")

        except Exception as e:
            config.logger.error(
                f"Ошибка создания QA цепочки для пользователя {user_id}: {e}"
            )
            import traceback

            config.logger.error(traceback.format_exc())

    async def initialize(self, force_reload: bool = False) -> bool:
        """Initialize RAG system."""

        config.logger.info("Initializing RAG system...")

        try:
            should_reload = force_reload or not os.path.exists(
                str(config.VECTOR_DB_PATH)
            )

            if should_reload:
                documents = await self.load_notion_documents_async()

                if not documents:
                    config.logger.error("No documents loaded")
                    return False

                chunks = self.split_documents(documents)

                if not chunks:
                    config.logger.error("No chunks created")
                    return False

                self.create_vectorstore(chunks)

            else:
                config.logger.info("Loading existing FAISS...")
                self.load_vectorstore()

            config.logger.info("RAG initialized successfully!")
            return True

        except Exception as e:
            config.logger.error(f"Initialization error: {e}")
            import traceback

            config.logger.error(traceback.format_exc())
            return False

    def query(self, question: str, user_id: int) -> Dict:
        """Optimized query with source-based image extraction."""

        try:
            cache_key = self._generate_cache_key(question, user_id)
            cached = self._get_from_cache(cache_key)
            if cached:
                return cached

            if user_id not in self.qa_chains:
                self.create_qa_chain(user_id)

            qa_chain = self.qa_chains[user_id]

            response = qa_chain.invoke({"question": question})

            answer = response.get("answer", "")
            sources = response.get("source_documents", [])

            # -- DEBUG PART --
            print(f"\nDEBUG QUERY: '{question}'")
            print(f"Sources found: {len(sources)}")
            for idx, doc in enumerate(sources):
                has_img = "img_" in doc.page_content
                print(
                    f"   [{idx + 1}] ...{doc.page_content[:40]}... (Has image? {has_img})"
                )
            # -----

            final_images = []
            seen_urls = set()

            for doc in sources:
                chunk_img_map = doc.metadata.get("image_map", {})

                if not chunk_img_map:
                    continue

                found_ids = re.findall(r"(img_[a-f0-9]{8})", doc.page_content)

                for img_id in found_ids:
                    if img_id in chunk_img_map:
                        url = chunk_img_map[img_id]
                        if url not in seen_urls:
                            final_images.append(url)
                            seen_urls.add(url)

            clean_answer = re.sub(r"\(?img_[a-f0-9]{8}\)?", "", answer)
            clean_answer = re.sub(r"!\[.*?\]\(.*?\)", "", clean_answer)
            clean_answer = clean_answer.strip()

            result = {
                "answer": clean_answer,
                "images": final_images,
                "sources": sources,
            }

            self._save_to_cache(cache_key, result)

            config.logger.info(
                f"Answer generated. Found {len(final_images)} images in context."
            )

            return result

        except Exception as e:
            config.logger.error(f"Query error: {e}")
            import traceback

            config.logger.error(traceback.format_exc())

            return {
                "answer": "Error occurred. Try /clear or rephrase the question.",
                "images": [],
                "sources": [],
            }

    def clear_memory(self, user_id: int):
        """Memory cleared."""

        if user_id in self.qa_chains:
            self.qa_chains[user_id].memory.clear()
            self._search_cache.clear()
            config.logger.info(f"Memory cleared for user {user_id}")


rag_system = RAGSystem()
