from langchain_community.vectorstores import Chroma
from langchain_text_splitters import (
    Language,
    RecursiveCharacterTextSplitter,
    TextSplitter,
)
import os

import shared.file_utils as U
import questllama.core.utils.logger as L
from questllama.core.retrievers import HybridRetriever
from questllama.core.retrievers import SimpleRetriever
from shared import config as C
from langchain.retrievers import BM25Retriever, EnsembleRetriever


class RetrievelSearchModels:
    vectorstores = ["chroma"]
    textsplitters = ["recursive"]
    retrievers = ["simple", "hybrid"]  # hybrid does semantic as well as keyword search

    # Local variables
    retriever = None
    _hybrid = None
    _simple = None

    def __init__(self, skill_library):
        self.logger = L.QuestLlamaLogger("OllamaAPI")

        self.action_files = U.read_skill_library(skill_library)
        self.logger.log(
            "info",
            f"Skill Library. Read {len(self.action_files)} javascript files.",
            "chromadb",
        )

    def get_hybrid_search(self, vectorstore, splitter, weights):
        if vectorstore not in self.vectorstores:
            raise Exception("Vector store not supported.")

        if splitter not in self.textsplitters:
            raise Exception("Unrecognised text splitter")

        if self.retriever is not None:
            return self.retriever

        # Parse the documents
        docs = self.get_documents(
            self.action_files,
            splitter=RecursiveCharacterTextSplitter.from_language(
                chunk_size=C.CHUNK_SIZE,
                chunk_overlap=C.CHUNK_OVERLAP,
                language=Language.JS,
            )
            if splitter in self.textsplitters
            else self.raiser(Exception("Unsupported splitter")),
        )

        embedding_function = C.EMBEDDING()
        # Check if the persistence directory exists
        if os.path.exists(C.DB_DIR):
            # Load Chroma from the existing directory
            vectorstore = Chroma(
                persist_directory=C.DB_DIR, embedding_function=embedding_function
            )
        else:
            # Load Chroma from documents and persist to disk if the directory does not exist
            vectorstore = Chroma.from_documents(
                documents=docs,
                embedding=embedding_function,
                persist_directory=C.DB_DIR,
            )

        # Semantic Search
        embedded_retriever = vectorstore.as_retriever(
            search_kwargs={"k": C.K}, search_type=C.SEARCH_TYPE
        )

        # Keyword Search
        keyword_retriever = BM25Retriever.from_documents(docs)
        keyword_retriever.k = C.K

        # Ensemble retriever
        retriever = EnsembleRetriever(
            retrievers=[embedded_retriever, keyword_retriever], weights=weights
        )
        return retriever

    def get_documents(self, files, splitter: TextSplitter):
        # create chunks
        return splitter.create_documents([doc[1] for doc in files])

    def get_simple_search(self):
        """
        Reads JavaScript files from the skill library stored in a vector store.
        The vector store will be used for information retrieval with the LLM.

        Returns:
            tuple: A tuple containing the vectorstore and the final retriever.
        """

        # FIXME is chunk_size at optimal value?
        js_splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.JS, chunk_size=C.CHUNK_SIZE, chunk_overlap=C.CHUNK_OVERLAP
        )

        embedding_function = C.EMBEDDING()
        # Check if the persistence directory exists
        if os.path.exists(C.DB_DIR):
            # Load Chroma from the existing directory
            vectorstore = Chroma(
                persist_directory=C.DB_DIR, embedding_function=embedding_function
            )
        else:
            js_docs = js_splitter.create_documents(
                [doc[1] for doc in self.action_files]
            )

            # Load Chroma from documents and persist to disk if the directory does not exist
            vectorstore = Chroma.from_documents(
                documents=js_docs,
                embedding=embedding_function,
                persist_directory=C.DB_DIR,
            )

        base_retriever = vectorstore.as_retriever(
            search_kwargs={"k": C.K}, search_type=C.SEARCH_TYPE
        )

        return base_retriever

    def get_retriever(self, query_type):
        # This code initializes and returns a retriever object based on the specified
        # query type and retriever configuration, either hybrid or simple.
        if self.retriever is None:
            if C.RETRIEVER == "hybrid":
                if self._hybrid is None:
                    self._hybrid = self.get_hybrid_search(
                        vectorstore="chroma", splitter="recursive", weights=[0.5, 0.5]
                    )

                self.retriever = HybridRetriever(
                    base_retriever=self._hybrid, query_type=query_type
                )

            elif C.RETRIEVER == "simple":
                if self._simple is None:
                    self._simple = self.get_simple_search()

                self.retriever = SimpleRetriever(
                    base_retriever=self._simple, query_type=query_type
                )

        return self.retriever

    def raiser(ex):
        raise ex
