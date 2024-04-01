from langchain.embeddings import GPT4AllEmbeddings
from langchain.vectorstores import Chroma
from langchain import PromptTemplate
from langchain_text_splitters import (
    Language,
    RecursiveCharacterTextSplitter,
)
from langchain_core.callbacks.manager import (
    CallbackManagerForRetrieverRun
)
from langchain.chains import RetrievalQA
from langchain.llms import Ollama
from langchain.schema import HumanMessage, SystemMessage
import os
from langchain_core.vectorstores import BaseRetriever, VectorStoreRetriever
from typing import List
import re

from pydantic import Field
import questllama.core.utils.file_utils as U
import questllama.core.utils.log_utils as L
from shared import BaseChatProvider, config as C
from shared.messages import QuestllamaMessage
from langchain_core.documents import Document



CRITIC = "critic"
ACTION = "action"
SKILL = 'skill'



class CustomRetriever(BaseRetriever):
    base_retriever: VectorStoreRetriever = None
    query_type: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _get_relevant_documents(self, query: str, *, run_manager: CallbackManagerForRetrieverRun) -> List[Document]:
        """
        _get_relevant_documents is function of BaseRetriever implemented here

        :param query: String value of the query

        """
        if self.query_type == CRITIC:
            return []

        if self.query_type == ACTION:
            pattern = r"Task:.*\n"
            match = re.search(pattern, query)
            if match:
                extracted_text = match.group()[6:]
            
            assert(len(extracted_text) > 2)
            # This method now calls the internal method that performs the actual retrieval
            documents = self.base_retriever._get_relevant_documents(query=extracted_text, run_manager=run_manager)

            return documents

