from langchain_core.callbacks.manager import CallbackManagerForRetrieverRun
from typing import List
from langchain_core.documents import Document
from langchain.retrievers import EnsembleRetriever

from .base_retriever import QuestllamaBaseRetriever


class HybridRetriever(QuestllamaBaseRetriever):
    base_retriever: EnsembleRetriever = None
    query_type: str

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
