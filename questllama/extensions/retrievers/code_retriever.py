from langchain_core.callbacks.manager import CallbackManagerForRetrieverRun
from langchain_core.vectorstores import VectorStoreRetriever
from typing import List, Optional
from langchain_core.documents import Document
from ragatouille import RAGPretrainedModel
from langchain.vectorstores import FAISS

import shared.config as Config
from .retrievers import QuestllamaBaseRetriever
import os

import questllama.core.utils.file_utils as U
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        if self.reranker is None:
            self.reranker = RAGPretrainedModel.from_pretrained("colbert-ir/colbertv2.0")

        task = self.get_task(query)
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
        


def get_base_retriever():
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
    docs_processed = _split_documents(
        CHUNK_SIZE, RAW_KNOWLEDGE_BASE, EMBEDDING_MODEL_NAME
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




def _split_documents(
    chunk_size: int,
    knowledge_base: List[LangchainDocument],
    tokenizer_name: Optional[str],
) -> List[LangchainDocument]:
    """
    Split documents into chunks of maximum size `chunk_size` tokens and return a list of documents.
    """   
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
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)

    # FIXME: Is it necessary to pass the separators here? Try without them.
    text_splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
        tokenizer,
        chunk_size=chunk_size,
        chunk_overlap=int(chunk_size / 10),
        add_start_index=True,
        strip_whitespace=True,
        separators=JAVASCRIPT_SEPARATORS,
    )

    docs_processed = []
    for doc in knowledge_base:
        docs_processed += text_splitter.split_documents([doc])

    # Remove duplicates
    unique_texts = {}
    docs_processed_unique = []
    for doc in docs_processed:
        if doc.page_content not in unique_texts:
            unique_texts[doc.page_content] = True
            docs_processed_unique.append(doc)

    return docs_processed_unique
