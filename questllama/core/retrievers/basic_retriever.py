from langchain_core.callbacks.manager import CallbackManagerForRetrieverRun
from langchain_core.vectorstores import BaseRetriever, VectorStoreRetriever
from typing import List
from langchain_core.documents import Document



class SimpleRetriever(BaseRetriever):
    base_retriever: VectorStoreRetriever = None
    query_type: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        documents = super()._get_relevant_documents(
            query=query, run_manager=run_manager
        )
        return documents

