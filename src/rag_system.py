import asyncio
import hashlib
import os
from typing import Dict, List, Optional

from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_ollama import OllamaLLM

import config
from markdown_cleaner import MarkdownCleaner
from notion_api_interactor import fetch_all_paginated_results, make_md_from_block


class RAGSystem:
    """Optimized RAG system with caching and parallel processing"""

    def __init__(self):
        self.vectorstore = None
        self.qa_chains = {}

        self._search_cache = {}
        self._cache_max_size = 100

        self.max_context_messages = 6
        self.max_tokens_per_context = 1500

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
            temperature=0,
            num_ctx=1536,
            num_predict=384,
            repeat_penalty=1.1,
            top_k=40,
            top_p=0.9,
            stop=["<|end_of_text|>", "\nВОПРОС:", "ВОПРОС:"],
            # timeout=60.0,
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

    async def load_notion_documents_async(self) -> List:
        """Async loading of documents from Notion."""

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

                for block in all_blocks:
                    text_chunk = make_md_from_block(block)
                    text_parts.append(text_chunk)

                full_text = "".join(text_parts)

                if not full_text.strip():
                    continue

                doc = Document(
                    page_content=full_text,
                    metadata={
                        "title": page_title,
                        "source": page_url,
                        "doc_id": i,
                        "id": page_id,
                        "char_count": len(full_text),
                    },
                )
                documents.append(doc)

            config.logger.info(f"Statistics: {len(documents)} documents loaded")

            config.logger.info("Cleaning documents...")
            documents = MarkdownCleaner.clean_documents(documents)
            config.logger.info(f"After cleaning: {len(documents)} documents")

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
            length_function=len,
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

            config.logger.info(
                f"FAISS index saved: {self.vectorstore.index.ntotal} vectors"
            )

        except Exception as e:
            config.logger.error(f"Error creating vectorstore: {e}")
            raise

    def load_vectorstore(self):
        """Load vectorstore."""

        load_path = str(config.VECTOR_DB_PATH)

        if not os.path.exists(load_path):
            raise FileNotFoundError(f"FAISS index not found at {load_path}")

        try:
            self.vectorstore = FAISS.load_local(
                load_path,
                embeddings=self.embeddings,
                allow_dangerous_deserialization=True,
            )

            index_size = self.vectorstore.index.ntotal
            config.logger.info(f"FAISS index loaded: {index_size} vectors")

        except Exception as e:
            config.logger.error(f"Error loading FAISS: {e}")
            raise

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

            prompt_template = """КОНТЕКСТ:
{context}

ВОПРОС: {question}

ОТВЕТ (кратко и точно):"""

            PROMPT = PromptTemplate(
                template=prompt_template, input_variables=["context", "question"]
            )

            memory = ConversationBufferWindowMemory(
                k=self.max_context_messages,
                memory_key="chat_history",
                return_messages=True,
                output_key="answer",
            )

            retriever = self.vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={
                    "k": 3,
                },
            )

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
            config.logger.info(f"QA chain successfully created for user {user_id}")

        except Exception as e:
            config.logger.error(f"Error creating QA chain for user {user_id}: {e}")
            import traceback

            config.logger.error(traceback.format_exc())

    def initialize(self, force_reload: bool = False) -> bool:
        """Initialize RAG system."""

        config.logger.info("Initializing RAG system...")

        try:
            should_reload = force_reload or not os.path.exists(
                str(config.VECTOR_DB_PATH)
            )

            if should_reload:
                headers = {
                    "Authorization": f"Bearer {config.NOTION_TOKEN}",
                    "Content-Type": "application/json",
                    "Notion-Version": "2022-06-28",
                }
                search_params = {"filter": {"value": "page", "property": "object"}}
                search_url = "https://api.notion.com/v1/search"

                all_pages = fetch_all_paginated_results(
                    search_url, headers, "POST", search_params
                )

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
                    all_blocks = fetch_all_paginated_results(
                        blocks_url, headers, "GET", None
                    )

                    text_parts = []

                    for block in all_blocks:
                        text_parts.append(make_md_from_block(block))

                    full_text = "".join(text_parts)
                    if full_text.strip():
                        doc = Document(
                            page_content=full_text,
                            metadata={
                                "title": page_title,
                                "source": page_url,
                                "doc_id": i,
                                "id": page_id,
                                "char_count": len(full_text),
                            },
                        )
                        documents.append(doc)

                if not documents:
                    return False

                documents = MarkdownCleaner.clean_documents(documents)
                chunks = self.split_documents(documents)

                if not chunks:
                    return False

                self.create_vectorstore(chunks)

            else:
                self.load_vectorstore()

            return True

        except Exception as e:
            config.logger.error(f"Initialization error: {e}")
            return False

    def query(self, question: str, user_id: int) -> Dict:
        """Optimized query with caching."""

        try:
            cache_key = self._generate_cache_key(question, user_id)
            cached_result = self._get_from_cache(cache_key)

            if cached_result:
                config.logger.info(f"Cache HIT for user {user_id}")
                return cached_result

            config.logger.info(f"Cache MISS - processing query for user {user_id}")

            if user_id not in self.qa_chains:
                config.logger.info(f"Creating QA chain for user {user_id}")
                self.create_qa_chain(user_id)

            qa_chain = self.qa_chains[user_id]

            response = qa_chain.invoke({"question": question})

            answer = response.get("answer", "")
            sources = response.get("source_documents", [])

            result = {"answer": answer, "sources": sources}

            self._save_to_cache(cache_key, result)

            config.logger.info(
                f"Answer generated: {len(answer)} chars, {len(sources)} sources"
            )

            return result

        except Exception as e:
            config.logger.error(f"Query error: {e}")
            import traceback

            config.logger.error(traceback.format_exc())

            return {
                "answer": "Error occurred. Try /clear or rephrase the question.",
                "sources": [],
            }

    def clear_memory(self, user_id: int):
        """Memory cleared."""

        if user_id in self.qa_chains:
            self.qa_chains[user_id].memory.clear()
            config.logger.info(f"Memory cleared for user {user_id}")


rag_system = RAGSystem()
