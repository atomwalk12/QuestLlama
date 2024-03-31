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
  # Hypothetical base class

from langchain_core.callbacks.manager import (
    AsyncCallbackManagerForRetrieverRun,
    CallbackManagerForRetrieverRun,
    Callbacks,
)
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from langchain_core.documents import Document
import re

import questllama.utils as U

import os
import sys


class CustomRetriever(BaseRetriever):
    base_retriever: VectorStoreRetriever = None
    last_retrieved_docs: List = []



    def _get_relevant_documents(self, query: str, *, run_manager: CallbackManagerForRetrieverRun) -> List[Document]:
        """
        _get_relevant_documents is function of BaseRetriever implemented here

        :param query: String value of the query

        """


        
        pattern = r"Task:.*\n"
        match = re.search(pattern, query)
        if match:
            extracted_text = match.group()[6:]
            print(extracted_text)
        # This method now calls the internal method that performs the actual retrieval
        documents = self.base_retriever._get_relevant_documents(query=extracted_text, run_manager=run_manager)
        # Store the retrieved documents for later access
        self.last_retrieved_docs = documents

        return documents




class SuppressStdout:
    def __enter__(self):
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr


def read_all_files(directory):
    results = []
    
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        
        # If it is a directory, recurse into it.
        if os.path.isdir(filepath):
            results += read_all_files(filepath)
            
        else:    # Otherwise, check the file's extension and add its path and content to the results list if it has .js extension.
            if filename.endswith('.js'):
                with open(filepath, 'r') as f:
                    results.append((filename, f.read()))
                
    return results


def append_elements_as_string(array):
    result = ''
    for element in array:
        if element[1] not in result:
            result += element[1] + ' '
    return result.strip()



if __name__ == "__main__":
    skill_library = read_all_files("skill_library/")


    chat = ChatOpenAI(openai_api_key="not-used", temperature=0.0)
    
    # assuming skill_library is a list of strings
    JS_CODE = append_elements_as_string(skill_library)
    tokens = chat.get_num_tokens(JS_CODE)
    print(tokens)


    js_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.JS, chunk_size=60, chunk_overlap=0
    )
    js_docs = js_splitter.create_documents([doc[1] for doc in skill_library])

    with SuppressStdout():
        vectorstore = Chroma.from_documents(documents=js_docs, embedding=GPT4AllEmbeddings())


    # Prompt
    while True:
        query = input("\nQuery: ")
        if query == "exit":
            break
        if query.strip() == "":
            continue

        # Prompt
        template = U.load_prompt("rag_prompt.txt")
        user = U.load_prompt("human_message.txt")
        QA_CHAIN_PROMPT = PromptTemplate(
            input_variables=["context", "question"],
            template=template,
        )

        query = user.format(task=query)

        # Initialize your base retriever
        # This is a placeholder - replace it with your actual vector store retriever initialization
        base_retriever = vectorstore.as_retriever(search_kwargs={"k": 10}, search_type='similarity')

        # Wrap it with the custom retriever
        custom_retriever = CustomRetriever(base_retriever=base_retriever, last_retrieved_docs=[])


        llm = Ollama(model="gpt-4", callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]), temperature=0.0)
        qa_chain = RetrievalQA.from_chain_type(
            llm,
            retriever=custom_retriever,
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
            return_source_documents=True
        )


        result = qa_chain({"query": query})

        tokenizer = Tokenizer.from_pretrained("deepseek-ai/deepseek-coder-33b-instruct")

        for doc in result['source_documents']:
            print(doc.page_content)

        # Tokenize the retrieved documents
        document_token_count = sum(len(tokenizer.encode(doc.page_content, add_special_tokens=True)) for doc in custom_retriever.last_retrieved_docs)

        # Tokenize the QA_CHAIN_PROMPT (assuming it's represented in a format that can be directly tokenized)
        prompt_token_count = len(tokenizer.encode(QA_CHAIN_PROMPT.template.format(context="", question=query), add_special_tokens=True))

        # Tokenize the QA_CHAIN_PROMPT (assuming it's represented in a format that can be directly tokenized)
        result_token_count = len(tokenizer.encode(result['result'], add_special_tokens=True))

        # Calculate the total token count
        total_token_count = document_token_count + prompt_token_count + result_token_count
        print(total_token_count)
    