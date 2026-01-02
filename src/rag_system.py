import os
import time

import requests
from typing import Dict, List

from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_ollama import OllamaLLM

import config
from notion_api_interactor import make_md_from_block, fetch_all_paginated_results


class AdvancedLocalRAGSystem:
    """Advanced Local RAG System with FAISS"""

    def __init__(self):
        self.vectorstore = None
        self.qa_chains = {}

        config.logger.info(f"Initializing embedding model: {config.EMBEDDING_MODEL}")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=config.EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

        config.logger.info("Embedding model has been loaded")

        config.logger.info(
            f"Initializing Ollama: {config.OLLAMA_BASE_URL}, model: {config.OLLAMA_MODEL}"
        )
        self.llm = OllamaLLM(
            model=str(config.OLLAMA_MODEL),
            base_url=str(config.OLLAMA_BASE_URL),
            temperature=0,
            num_ctx=2048,
            num_predict=512,
            repeat_penalty=1.1,
            top_k=40,
            top_p=0.9,
            stop=["<|end_of_text|>", "\nВОПРОС:", "ВОПРОС:"],
            timeout=300.0
        )
        config.logger.info("Ollama has been initialized")

    def load_notion_documents(self) -> List:
        config.logger.info("Loading local data from Notion API")

        headers = {
            'Authorization': f"Bearer {config.NOTION_TOKEN}",
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28'
        }
        search_params = {"filter": {"value": "page", "property": "object"}}
        search_url = 'https://api.notion.com/v1/search'

        try:
            all_pages = fetch_all_paginated_results(
                url=search_url,
                headers=headers,
                method="POST",
                params=search_params
            )

            if not all_pages:
                config.logger.warning("No pages found.")
                return []

            config.logger.info(f"Found {len(all_pages)} pages in Notion. Processing...")

            documents = []
            for i, page in enumerate(all_pages):
                page_id = page['id']
                page_url = page.get('url', '')
                page_title = "Untitled"
                props = page.get('properties', {})

                for key, value in props.items():
                    if value['type'] == 'title' and value['title']:
                        page_title = value['title'][0]['plain_text']
                        break

                config.logger.info(f"[{i}] Content loading: {page_title}({page_id}) from {page_url}) ")

                # Request for page children (paragraph, headers, etc)
                blocks_url = f'https://api.notion.com/v1/blocks/{page_id}/children'

                all_blocks = fetch_all_paginated_results(
                    url=blocks_url,
                    headers=headers,
                    method="GET"
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
                        "char_count": len(full_text)
                    }
                )
                documents.append(doc)

            total_chars = sum(len(doc.page_content) for doc in documents)
            avg_chars = total_chars / len(documents) if documents else 0

            config.logger.info("Statistics:")
            config.logger.info(f"- Total documents: {len(documents)}")
            config.logger.info(f"- Total characters: {total_chars:,}")
            config.logger.info(f"- Average per document: {avg_chars:.0f} chars")

            if documents:
                first_doc = documents[0]
                preview = first_doc.page_content[:200].replace("\n", " ")
                config.logger.info("First document preview:")
                config.logger.info(f"   Title: {first_doc.metadata.get('title')}")
                config.logger.info(f"   Content: {preview}...")

            time.sleep(2)
            return documents

        except Exception as e:
            config.logger.error(f"Error during loading documents from API: {e}")
            import traceback

            config.logger.error(traceback.format_exc())
            return []

    def split_documents(self, documents: List) -> List:
        if not documents:
            config.logger.error("No documents to split!")
            return []

        config.logger.info(f"Splitting {len(documents)} documents into chunks...")

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
            length_function=len,
            separators=config.SEPARATORS,
        )

        try:
            chunks = text_splitter.split_documents(documents)
            config.logger.info(f"Created {len(chunks)} chunks")

            if chunks:
                avg_chunk_size = sum(len(chunk.page_content) for chunk in chunks) / len(
                    chunks
                )
                config.logger.info(
                    f"Average chunk size: {avg_chunk_size:.0f} characters"
                )

            return chunks

        except Exception as e:
            config.logger.error(f"Error splitting documents: {e}")
            return []

    def create_vectorstore(self, chunks: List) -> None:
        if not chunks:
            config.logger.error("No chunks to create vectorstore!")
            return

        config.logger.info(f"Creating FAISS vectorstore with {len(chunks)} chunks...")

        config.logger.info("Sample chunks:")
        for i, chunk in enumerate(chunks[:3]):
            preview = chunk.page_content[:100].replace("\n", " ")
            config.logger.info(f"   Chunk {i + 1}: {preview}...")

        try:
            config.logger.info("Creating FAISS index...")
            self.vectorstore = FAISS.from_documents(
                documents=chunks,
                embedding=self.embeddings,
            )

            config.logger.info("FAISS index created")

            save_path = str(config.VECTOR_DB_PATH)
            config.logger.info(f"Saving FAISS index to {save_path}...")

            os.makedirs(save_path, exist_ok=True)

            self.vectorstore.save_local(save_path)

            config.logger.info(f"FAISS index saved to {save_path}")

            index_size = self.vectorstore.index.ntotal
            config.logger.info(f"FINAL COUNT: {index_size} vectors in index")

            if index_size == 0:
                config.logger.error("CRITICAL: Index created but has 0 vectors!")
            else:
                config.logger.info(f"SUCCESS! FAISS index has {index_size} vectors")

        except Exception as e:
            config.logger.error(f"Error creating vectorstore: {e}")
            import traceback

            config.logger.error(traceback.format_exc())
            raise

    def load_vectorstore(self):
        load_path = str(config.VECTOR_DB_PATH)
        config.logger.info(f"Loading FAISS index from {load_path}")

        if not os.path.exists(load_path):
            config.logger.error(f"FAISS index not found at {load_path}")
            raise FileNotFoundError(f"FAISS index not found at {load_path}")

        try:
            self.vectorstore = FAISS.load_local(
                load_path,
                embeddings=self.embeddings,
                allow_dangerous_deserialization=True,
            )

            index_size = self.vectorstore.index.ntotal

            if index_size == 0:
                config.logger.warning("FAISS index loaded but it's EMPTY (0 vectors)")
            else:
                config.logger.info(f"FAISS index loaded with {index_size} vectors")

        except Exception as e:
            config.logger.error(f"Error loading FAISS index: {e}")
            raise

    def create_qa_chain(self, user_id: int):
        if self.vectorstore is None:
            return

        condense_template = """История диалога: {chat_history}
Новый вопрос: {question}
Перефразируй вопрос так, чтобы он был понятен без истории, сохранив РУССКИЙ язык:"""

        CONDENSE_PROMPT = PromptTemplate.from_template(condense_template)

        prompt_template = """ИНСТРУКЦИЯ: Отвечай строго на РУССКОМ языке. Используй только предоставленный текст.
Если в тексте нет ответа, напиши "Информация отсутствует в Notion".

ТЕКСТ:
{context}

ВОПРОС: {question}
ОТВЕТ НА РУССКОМ:"""

        PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )

        memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True, output_key="answer"
        )

        try:
            retriever = self.vectorstore.as_retriever(
                search_type="mmr", search_kwargs={"k": 4, "lambda_mult": 0.6}
            )

            qa_chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=retriever,
                memory=memory,
                return_source_documents=True,
                condense_question_prompt=CONDENSE_PROMPT,
                combine_docs_chain_kwargs={"prompt": PROMPT},
                get_chat_history=lambda h: h,
                verbose=True,
            )
            self.qa_chains[user_id] = qa_chain
        except Exception as e:
            config.logger.error(f"Error: {e}")

    def initialize(self, force_reload: bool = False) -> bool:
        config.logger.info("Initializing RAG system...")

        try:
            should_reload = force_reload or not os.path.exists(
                str(config.VECTOR_DB_PATH)
            )

            if  should_reload:
                config.logger.info("Loading documents from Notion folder...")

                documents = self.load_notion_documents()
                if not documents:
                    config.logger.error("No documents loaded. Cannot initialize.")
                    return False

                config.logger.info(f"Loaded {len(documents)} documents from Notion")

                chunks = self.split_documents(documents)
                if not chunks:
                    config.logger.error("No chunks created. Cannot initialize.")
                    return False

                self.create_vectorstore(chunks)

            else:
                config.logger.info("Loading existing FAISS index...")
                self.load_vectorstore()

                index_size = self.vectorstore.index.ntotal
                config.logger.info(f"FAISS index has {index_size} vectors")

                if index_size == 0:
                    config.logger.warning(
                        "FAISS index is EMPTY! Reloading documents..."
                    )

                    documents = self.load_notion_documents()
                    if not documents:
                        config.logger.error("No documents found for reload.")
                        return False

                    chunks = self.split_documents(documents)
                    if not chunks:
                        config.logger.error("No chunks created.")
                        return False

                    self.create_vectorstore(chunks)

                    index_size = self.vectorstore.index.ntotal  # type: ignore
                    config.logger.info(f"After reload: {index_size} vectors")

            if self.vectorstore is None:
                config.logger.error("Vectorstore is None after initialization!")
                return False

            config.logger.info("RAG system initialized successfully!")
            return True

        except Exception as e:
            config.logger.error(f"Critical error during initialization: {e}")
            import traceback

            config.logger.error(traceback.format_exc())
            return False

    def query(self, question: str, user_id: int) -> Dict:
        try:
            if user_id not in self.qa_chains:
                config.logger.info(f"Creating new QA chain for user {user_id}")
                self.create_qa_chain(user_id)

            qa_chain = self.qa_chains[user_id]

            config.logger.info(
                f"Processing query from user {user_id}: {question[:50]}..."
            )

            response = qa_chain.invoke({"question": question})

            answer = response["answer"]
            sources = response.get("source_documents", [])

            config.logger.info(
                f"Generated answer ({len(answer)} chars) with {len(sources)} sources"
            )

            return {
                "answer": answer,
                "sources": sources,
            }

        except Exception as e:
            config.logger.error(f"Error processing query: {e}")
            import traceback

            config.logger.error(traceback.format_exc())

            return {
                "answer": "Sorry, an error occurred. Please try /clear or rephrase your question.",
                "sources": [],
            }

    def clear_memory(self, user_id: int):
        if user_id in self.qa_chains:
            self.qa_chains[user_id].memory.clear()
            config.logger.info(f"Memory cleared for user {user_id}")
        else:
            config.logger.warning(f"User {user_id} not found in qa_chains")


rag_system = AdvancedLocalRAGSystem()
