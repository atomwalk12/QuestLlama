from abc import abstractmethod
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import Optional, List, Tuple

from langchain.prompts.chat import (
    ChatPromptTemplate,
)
from transformers import AutoTokenizer
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.utils import DistanceStrategy
import os
import re
from shared import file_utils as U

import questllama.core.constants as tasks
from ragatouille import RAGPretrainedModel
from langchain_core.vectorstores import VectorStore
from langchain_core.language_models.llms import LLM


class CodeRetriever:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CodeRetriever, cls).__new__(cls)
        return cls._instance

    def __init__(self, chunk_size: int, embeddings: str, reranker: str):
        if not self._initialized:
            # Put your initialization code here
            RAW_KNOWLEDGE_BASE = self.read_knowledge_base()

            self.knowledge_index = self.load_embeddings(
                RAW_KNOWLEDGE_BASE,
                chunk_size=chunk_size,
                embedding_model_name=embeddings,
            )

            self.reranker = RAGPretrainedModel.from_pretrained(reranker)
            self._initialized = True

    @abstractmethod
    def answer_with_rag(
        task: str,
        template: ChatPromptTemplate,
        llm: LLM,
        knowledge_index: VectorStore,
        reranker: Optional[RAGPretrainedModel] = None,
        num_retrieved_docs: int = 30,
        num_docs_final: int = 7,
    ) -> Tuple[str, List[Document]]:
        """ """
        # Gather documents with retriever
        relevant_docs = knowledge_index.similarity_search(
            query=task, k=num_retrieved_docs
        )
        relevant_docs = [
            doc.page_content for doc in relevant_docs
        ]  # keep only the text

        # Optionally rerank results
        if reranker:
            relevant_docs = reranker.rerank(task, relevant_docs, k=num_docs_final)
            relevant_docs = [doc["content"] for doc in relevant_docs]

        relevant_docs = relevant_docs[:num_docs_final]

        # Build the final prompt
        context = "\nExtracted documents:\n"
        context += "".join(
            [f"Document {str(i)}:::\n" + doc for i, doc in enumerate(relevant_docs)]
        )

        final_prompt = template.format(context=context)

        # Redact an answer
        answer = llm.invoke(final_prompt)

        return answer, relevant_docs

    def read_knowledge_base(self):
        ## Read the dataset
        ds = U.read_skill_library("skill_library", full_path=True)
        ds = [{"text": elem[1], "source": elem[0]} for elem in ds]
        RAW_KNOWLEDGE_BASE = [
            Document(page_content=doc["text"], metadata={"source": doc["source"]})
            for doc in ds
        ]

        return RAW_KNOWLEDGE_BASE

    def load_embeddings(
        self,
        langchain_docs: List[Document],
        chunk_size: int,
        embedding_model_name: Optional[str],
    ) -> FAISS:
        """
        Creates a FAISS index from the given embedding model and documents. Loads the index directly if it already exists.

        Args:
            langchain_docs: list of documents
            chunk_size: size of the chunks to split the documents into
            embedding_model_name: name of the embedding model to use

        Returns:
            FAISS index
        """
        # load embedding_model
        embedding_model = HuggingFaceEmbeddings(
            model_name=embedding_model_name,
            multi_process=True,
            model_kwargs={"device": "cuda"},
            encode_kwargs={
                "normalize_embeddings": True
            },  # set True to compute cosine similarity
        )

        # Check if embeddings already exist on disk
        index_name = f"index_chunk:{chunk_size}_embeddings:{embedding_model_name.replace('/', '~')}"
        index_folder_path = f"./data/indexes/{index_name}/"
        if os.path.isdir(index_folder_path):
            return FAISS.load_local(
                index_folder_path,
                embedding_model,
                distance_strategy=DistanceStrategy.COSINE,
                allow_dangerous_deserialization=True,
            )
        else:
            print("Index not found, generating it...")

            docs_processed = self.split_documents(
                chunk_size,
                langchain_docs,
                embedding_model_name,
            )
            knowledge_index = FAISS.from_documents(
                docs_processed,
                embedding_model,
                distance_strategy=DistanceStrategy.COSINE,
            )
            knowledge_index.save_local(index_folder_path)
            return knowledge_index

    def split_documents(
        self,
        chunk_size: int,
        knowledge_base: List[Document],
        tokenizer_name: Optional[str],
    ) -> List[Document]:
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
        print(f"Tokenizer: {tokenizer_name}, Chunk Size: {chunk_size}")
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

    def get_task(self, query_type: str, prompt_template: ChatPromptTemplate):
        """
        Extracts task description from a given query string.
        """
        msgs = prompt_template[1:]
        for msg in msgs.messages:
            pattern = r"Task:.*\n" if query_type == tasks.ACTION else r"Final task:.*"
            match = re.search(pattern, msg.content)
            if match:
                extracted_text = (
                    match.group()[6:] if query_type == tasks.ACTION else match.group()[12:]
                )
                break

        assert len(extracted_text) > 2
        return extracted_text
