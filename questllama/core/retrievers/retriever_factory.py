from questllama.core.retrievers.code_retriever import CodeRetriever
from langchain.vectorstores import FAISS

import shared.config as Config
from .base_retriever import QuestllamaBaseRetriever
import os

import shared.file_utils as U
from shared import config as C
from langchain.docstore.document import Document as LangchainDocument
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.utils import DistanceStrategy


class RetrieverFactory:
    @staticmethod
    def create_retriever(retriever_type, query_type):
        if retriever_type == "code_search":
            return RetrieverFactory._get_code_retriever(query_type=query_type)
        else:
            raise Exception(f"Retriever type {retriever_type} not recognised.")

    @staticmethod
    def _get_code_retriever(query_type):
        base_retriever, KNOWLEDGE_VECTOR_DATABASE = (
            RetrieverFactory._get_base_retriever(CodeRetriever.JAVASCRIPT_SEPARATORS)
        )
        return CodeRetriever(
            query_type=query_type,
            base_retriever=base_retriever,
            knowledge_index=KNOWLEDGE_VECTOR_DATABASE,
        )

    @staticmethod
    def _get_base_retriever(separators):
        # read js files and map them to langchain document format
        action_files = U.read_skill_library(Config.SKILL_PATH, full_path=True)
        RAW_KNOWLEDGE_BASE = [
            LangchainDocument(page_content=doc[1], metadata={"source": doc[0]})
            for doc in action_files
        ]

        # chunk size > 128 not supported by the embedding model
        EMBEDDING_MODEL_NAME = (
            "flax-sentence-embeddings/st-codesearch-distilroberta-base"
        )
        CHUNK_SIZE = 128

        # split the files according to js separators
        docs_processed = QuestllamaBaseRetriever._split_documents(
            CHUNK_SIZE, RAW_KNOWLEDGE_BASE, EMBEDDING_MODEL_NAME, separators=separators
        )

        # only usable embedding model
        embedding_model = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL_NAME,
            multi_process=True,
            model_kwargs={"device": "cuda"},
            encode_kwargs={
                "normalize_embeddings": True
            },  # set True for cosine similarity
        )

        # Create and save/load the database
        if os.path.exists(C.DB_DIR):
            KNOWLEDGE_VECTOR_DATABASE = FAISS.load_local(
                C.DB_DIR, embedding_model, allow_dangerous_deserialization=True
            )
        else:
            KNOWLEDGE_VECTOR_DATABASE = FAISS.from_documents(
                docs_processed,
                embedding_model,
                distance_strategy=DistanceStrategy.COSINE,
            )
            KNOWLEDGE_VECTOR_DATABASE.save_local(C.DB_DIR)

        base_retriever = KNOWLEDGE_VECTOR_DATABASE.as_retriever(
            search_kwargs={"k": C.K}, search_type=C.SEARCH_TYPE
        )

        return base_retriever, KNOWLEDGE_VECTOR_DATABASE
