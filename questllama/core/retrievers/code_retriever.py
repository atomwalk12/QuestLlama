from array import array
from langchain_core.callbacks.manager import CallbackManagerForRetrieverRun
from langchain_core.vectorstores import VectorStoreRetriever
from typing import List, Optional
from langchain_core.documents import Document
from ragatouille import RAGPretrainedModel
from langchain.vectorstores import FAISS

import shared.config as Config
from .base_retriever import QuestllamaBaseRetriever
import os

import shared.file_utils as U
from shared import config as C
from langchain.docstore.document import Document as LangchainDocument
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.utils import DistanceStrategy
from transformers import AutoTokenizer


class CodeRetriever(QuestllamaBaseRetriever):
    TOP_K_GREEDY = 30
    TOP_K = Config.K
    knowledge_index: FAISS = None
    base_retriever: VectorStoreRetriever = None
    query_type: str
    reranker: RAGPretrainedModel = None
    JAVASCRIPT_SEPARATORS = [
        "\nfunction ",
        "\nconst ",
        "\nlet ",
        "\nvar ",
        "\nclass ",
        "\nif ",
        "\nfor ",
        "\nwhile ",
        "\nswitch ",
        "\ncase ",
        "\ndefault ",
        "\n\n",
        "\n",
        " ",
        "",
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        documents = super()._get_relevant_documents(
            query=query, run_manager=run_manager
        )
        for doc in documents:
            print(doc.page_content + "\n\n")
        return documents

    def get_documents(self, query, run_manager):
        task = self.get_task(query)

        if self.reranker is None:
            self.reranker = RAGPretrainedModel.from_pretrained("colbert-ir/colbertv2.0")

        relevant_docs = self.knowledge_index.similarity_search(
            query=task, k=self.TOP_K_GREEDY
        )
        relevant_docs = [
            doc.page_content for doc in relevant_docs
        ]  # keep only the text

        # Optionally rerank results
        if self.reranker:
            print("=> Reranking documents...")
            relevant_docs = self.reranker.rerank(task, relevant_docs, k=self.TOP_K)
            relevant_docs = [doc["content"] for doc in relevant_docs]

        relevant_docs = relevant_docs[: self.TOP_K]

        # Build the final prompt
        print(f"\nQuery: {task}\nExtracted documents:\n")

        for i, doc in enumerate(relevant_docs):
            print(f"Document {str(i)}:::\n" + doc)

        langchain_docs = [Document(page_content=doc) for doc in relevant_docs]

        return langchain_docs
