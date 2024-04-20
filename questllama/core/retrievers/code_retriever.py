from langchain_core.callbacks.manager import CallbackManagerForRetrieverRun
from langchain_core.vectorstores import VectorStoreRetriever
from typing import List
from langchain_core.documents import Document
from ragatouille import RAGPretrainedModel
from langchain_community.vectorstores import FAISS

import shared.config as Config
from .base_retriever import QuestllamaBaseRetriever


class CodeRetriever(QuestllamaBaseRetriever):
    TOP_K_GREEDY = 30
    TOP_K = Config.K
    knowledge_index: FAISS = None
    base_retriever: VectorStoreRetriever = None
    query_type: str
    reranker: RAGPretrainedModel = None

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
