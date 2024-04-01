from langchain_community.chat_models import ChatOpenAI
from langchain import PromptTemplate
from langchain.document_loaders import OnlinePDFLoader
from langchain.vectorstores import Chroma
from langchain.embeddings import GPT4AllEmbeddings
from langchain import PromptTemplate
from langchain.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import RetrievalQA
from langchain_text_splitters import (
    Language,
    RecursiveCharacterTextSplitter,
)
from tokenizers import Tokenizer
from langchain_core.vectorstores import BaseRetriever, VectorStoreRetriever
from pydantic import BaseModel, Field
# Hypothetical base class

from langchain_core.callbacks.manager import (
    AsyncCallbackManagerForRetrieverRun,
    CallbackManagerForRetrieverRun,
    Callbacks,
)
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from langchain_core.documents import Document
import re

import questllama.core.utils as U
import pkg_resources
import os
import sys
import shared.config as C
import questllama.core.utils.file_utils as U


CRITIC = "critic"
ACTION = "action"


class RAG:
    def load_prompt(self, prompt):
        # FIXME
        package_path = pkg_resources.resource_filename("questllama", "core")
        return U.load_text(f"{package_path}/prompts/temp/{prompt}")

    def get_vectorstore(self, files):
        embedding_function = GPT4AllEmbeddings()
        # Check if the persistence directory exists
        if os.path.exists(C.DB_DIR):
            # Load Chroma from the existing directory
            vectorstore = Chroma(
                persist_directory=C.DB_DIR, embedding_function=embedding_function
            )
        else:
            # Load Chroma from documents and persist to disk if the directory does not exist
            vectorstore = Chroma.from_documents(
                documents=files,
                embedding=embedding_function,
                persist_directory=C.DB_DIR,
            )

        return vectorstore

    def get_documents(self):
        # FIXME parameters
        js_splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.JS, chunk_size=60, chunk_overlap=0
        )
        js_docs = js_splitter.create_documents([doc[1] for doc in skill_library])
        return js_docs

RETRIEVER_TYPE = ''

class CustomRetriever(BaseRetriever):
    base_retriever: VectorStoreRetriever = None
    last_retrieved_docs: List = []
    _my_type: str = CRITIC

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        """
        _get_relevant_documents is function of BaseRetriever implemented here

        :param query: String value of the query

        """
        if RETRIEVER_TYPE == CRITIC:
            return []

        if RETRIEVER_TYPE == ACTION:
            pattern = r"Task:.*\n"
            match = re.search(pattern, query)
            if match:
                extracted_text = match.group()[6:]
                print(extracted_text)
            # This method now calls the internal method that performs the actual retrieval
            documents = self.base_retriever._get_relevant_documents(
                query=extracted_text, run_manager=run_manager
            )
            # Store the retrieved documents for later access
            self.last_retrieved_docs = documents

            return documents

        raise Exception("unknown operation")


if __name__ == "__main__":
    _TYPE = CRITIC

    skill_library = U.read_skill_library("skill_library/")

    rag = RAG()
    js_docs = rag.get_documents()

    vectorstore = rag.get_vectorstore(js_docs)

    # Prompt
    while True:
        # i.e. Mine 1 wood log
        query = input("\nQuery: ")
        if query == "exit":
            break
        if query.strip() == "":
            continue

        # Prompt
        template = rag.load_prompt(_TYPE + "/system.txt")
        user = rag.load_prompt(_TYPE + "/user.txt")
        QA_CHAIN_PROMPT = PromptTemplate(
            input_variables=["context", "question"],
            template=template,
        )

        query = user.format(task=query)

        # Initialize your base retriever
        # This is a placeholder - replace it with your actual vector store retriever initialization
        base_retriever = vectorstore.as_retriever(
            search_kwargs={"k": 10}, search_type="similarity"
        )

        # Wrap it with the custom retriever
        custom_retriever: CustomRetriever = CustomRetriever(
            base_retriever=base_retriever, last_retrieved_docs=[]
        )

        llm = Ollama(
            model="gpt-4",
            callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
            temperature=0.0,
        )
        qa_chain = RetrievalQA.from_chain_type(
            llm,
            retriever=custom_retriever,
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
            return_source_documents=True,
        )

        RETRIEVER_TYPE = _TYPE

        result = qa_chain({"query": query})
