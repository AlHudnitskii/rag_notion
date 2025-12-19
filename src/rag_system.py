import os
from typing import Dict, List

from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaLLM

import config


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
            num_ctx=4096,
            num_predict=512,
            repeat_penalty=1.1,
            top_k=40,
            top_p=0.9,
            stop=["<|end_of_text|>", "\nВОПРОС:", "ВОПРОС:"],
        )
        config.logger.info("Ollama has been initialized")

    def load_notion_documents(self) -> List:
        export_path = "./notion"

        config.logger.info(f"Loading local data from folder: {export_path}")

        if not os.path.exists(export_path):
            config.logger.error(f"FOLDER NOT FOUND: {export_path}")
            config.logger.error("Create 'notion' folder and add your .md files")
            return []

        md_files = []
        for root, dirs, files in os.walk(export_path):
            md_files.extend([os.path.join(root, f) for f in files if f.endswith(".md")])

        if not md_files:
            config.logger.error(f"NO .md FILES FOUND in {export_path}")
            config.logger.error("Export your Notion database as Markdown & CSV")
            return []

        config.logger.info(f"Found {len(md_files)} .md files")

        config.logger.info("Sample files:")
        for f in md_files[:5]:
            config.logger.info(f"   • {f}")
        if len(md_files) > 5:
            config.logger.info(f"   ... and {len(md_files) - 5} more")

        try:
            config.logger.info("Loading documents with DirectoryLoader...")
            loader = DirectoryLoader(
                export_path,
                glob="**/*.md",
                loader_cls=TextLoader,
                loader_kwargs={"encoding": "utf-8"},
                show_progress=True,
                use_multithreading=True,
            )

            documents = loader.load()

            if not documents:
                config.logger.error("FILES FOUND BUT THEY ARE EMPTY!")
                return []

            config.logger.info(f"SUCCESS! Loaded {len(documents)} documents.")

            total_chars = sum(len(doc.page_content) for doc in documents)
            avg_chars = total_chars / len(documents) if documents else 0

            config.logger.info("Statistics:")
            config.logger.info(f"- Total documents: {len(documents)}")
            config.logger.info(f"- Total characters: {total_chars:,}")
            config.logger.info(f"- Average per document: {avg_chars:.0f} chars")

            empty_docs = [
                i
                for i, doc in enumerate(documents)
                if len(doc.page_content.strip()) == 0
            ]
            if empty_docs:
                config.logger.warning(f"Found {len(empty_docs)} empty documents!")

            config.logger.info("Enhancing metadata...")
            for i, doc in enumerate(documents):
                source = doc.metadata.get("source", "")
                filename = os.path.basename(source)

                clean_name = filename.replace(".md", "")
                parts = clean_name.rsplit(" ", 1)
                if len(parts) == 2 and len(parts[1]) == 32:
                    clean_name = parts[0]

                doc.metadata = {
                    "title": clean_name,
                    "source": source,
                    "doc_id": i,
                    "char_count": len(doc.page_content),
                }

            config.logger.info("Metadata enhanced")

            if documents:
                first_doc = documents[0]
                preview = first_doc.page_content[:200].replace("\n", " ")
                config.logger.info("First document preview:")
                config.logger.info(
                    f"   Title: {first_doc.metadata.get('title', 'N/A')}"
                )
                config.logger.info(f"   Content: {preview}...")

            return documents

        except Exception as e:
            config.logger.error(f"❌ Error loading documents: {e}")
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

            if should_reload:
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
