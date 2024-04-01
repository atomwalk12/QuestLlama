from langchain.callbacks.manager import CallbackManager
from langchain.embeddings import GPT4AllEmbeddings
from langchain.vectorstores import Chroma
from langchain_community.chat_models import ChatOpenAI
from langchain import PromptTemplate
from langchain_text_splitters import (
    Language,
    RecursiveCharacterTextSplitter,
)
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_core.callbacks.manager import CallbackManagerForRetrieverRun
from langchain.chains import RetrievalQA
from langchain_core.vectorstores import BaseRetriever, VectorStoreRetriever
from typing import List
from langchain_core.documents import Document
from tokenizers import Tokenizer
from langchain.llms import Ollama
from langchain.schema import AIMessage, HumanMessage, SystemMessage

import re

import questllama.core.utils.file_utils as U
import questllama.core.utils.log_utils as L
from shared import BaseChatProvider, config as C


class QuestllamaClientProvider(BaseChatProvider):
    """A client provider for Voyager. This class allows you to get a ChatOpenAI client."""

    retriever = None
    logger_callback_added = False

    def __init__(self, model_name, temperature, request_timeout):
        super().__init__(
            model_name=model_name,
            temperature=temperature,
            request_timeout=request_timeout,
        )
        self.logger = L.QuestLlamaLogger("OllamaAPI")

        self.client = self._get_client(model_name, temperature, request_timeout)

        if QLCP.retriever is None:
            QLCP.retriever = self.get_retriever(C.SKILL_PATH, 10, "similarity")

    def generate(self, messages):
        """Generate messages using the LLM. As backend it defaults to Ollama."""
        assert len(messages) <= 2
        assert isinstance(messages[0], SystemMessage)
        QA_CHAIN_PROMPT = PromptTemplate(
            input_variables=["context", "question"],
            template=messages[0].content,  # system prompt
        )

        qa_chain = RetrievalQA.from_chain_type(
            self.client,
            retriever=QLCP.retriever,
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
            return_source_documents=True,
        )

        result = qa_chain({"query": messages[1]})  # user prompt
        self.check_token_count(
            messages=messages, qa_prompt=QA_CHAIN_PROMPT, result=result
        )

        return result["result"]

    def get_retriever(self, lib_path="skill_library", k=10, search_type="similarity"):
        """
        Reads JavaScript files from the skill library stored in a vector store.
        The vector store will be used for information retrieval with the LLM.

        Returns:
            tuple: A tuple containing the vectorstore and the final retriever.
        """
        files = U.read_skill_library(lib_path)
        self.logger.log("info", f"Skill Library. Read {len(files)} javascript files.")

        # FIXME is chunk_size at optimal value?
        js_splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.JS, chunk_size=60, chunk_overlap=0
        )
        js_docs = js_splitter.create_documents([doc[1] for doc in files])

        with L.SuppressStdout():
            vectorstore = Chroma.from_documents(
                documents=js_docs, embedding=GPT4AllEmbeddings()
            )

        base_retriever = vectorstore.as_retriever(
            search_kwargs={"k": k}, search_type=search_type
        )

        # Wrap it with the custom retriever
        retriever = CustomRetriever(
            base_retriever=base_retriever, last_retrieved_docs=[]
        )
        return retriever

    def _get_client(self, model_name="gpt-4", temperature=0.0, request_timeout=120):
        """
        Returns a new instance of the ChatOpenAI client with the provided parameters.
        The handle is used to redirect output to stdout during the output generation.
        """
        callbacks = CallbackManager([])

        # Add LoggerCallbackHandler only if it hasn't been added before
        if not QLCP.logger_callback_added:
            callbacks.add_handler(L.LoggerCallbackHandler())
            QLCP.logger_callback_added = (
                True  # Mark as added in order to write data only once
            )

        return Ollama(
            temperature=temperature,
            model=model_name,
            callback_manager=callbacks,
        )

        # Todo remove
        # return ChatOpenAI(
        #     base_url="http://localhost:11434/v1/",
        #     temperature=temperature,
        #     request_timeout=request_timeout,
        #     model_name=model_name,
        #     streaming=True,
        #     callback_manager=callbacks,
        # )

    def check_token_count(self, user, qa_system, result):
        tokenizer = Tokenizer.from_pretrained(C.TOKENIZER)
        # Find out the total number of tokens in the retrieved documents
        document_token_count = 0
        for doc in self.result["source_documents"]:
            document_token_count += len(
                tokenizer.encode(doc.page_content, add_special_tokens=True)
            )
            print(f"Document Content: {doc.page_content}")

        # Find out the number of tokens found in the system and user prompts together
        prompt_token_count = len(
            tokenizer.encode(
                qa_system.template.format(
                    context="", question=user
                ),  # user prompt, context are the documents
                add_special_tokens=True,
            )
        )

        # Total number of tokens stored in the final result
        result_token_count = len(
            tokenizer.encode(result["result"], add_special_tokens=True)
        )

        # Calculate the total token count
        total_token_count = (
            document_token_count + prompt_token_count + result_token_count
        )

        self.logger.log(
            "info", f"Context window OK: ${total_token_count} < ${C.CONTEXT_SIZE}"
        ) if total_token_count < C.CONTEXT_SIZE else self.logger.log(
            "error",
            f"Context window not OK: ${total_token_count} > ${C.CONTEXT_SIZE}",
        )

        assert total_token_count > C.CONTEXT_SIZE


QLCP = QuestllamaClientProvider


class CustomRetriever(BaseRetriever):
    base_retriever: VectorStoreRetriever = None
    last_retrieved_docs: List = []

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        """
        _get_relevant_documents is function of BaseRetriever implemented here
        """

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
