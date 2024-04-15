import re
from langchain_core.callbacks.manager import CallbackManagerForRetrieverRun
from langchain_core.vectorstores import BaseRetriever
from typing import List
from langchain_core.documents import Document
from langchain.retrievers import EnsembleRetriever
import questllama.core.constants as tasks
from langchain.docstore.document import Document as LangchainDocument
from array import array
from typing import Optional
from langchain_text_splitters import RecursiveCharacterTextSplitter
from transformers import AutoTokenizer


class QuestllamaBaseRetriever(BaseRetriever):
    base_retriever: EnsembleRetriever = None
    query_type: str
    simple_tasks = [
        tasks.CRITIC,
        tasks.SKILL,
        tasks.CURRICULUM,
        tasks.CURRICULUM_QA_STEP2_ANSWER_QUESTIONS,
        tasks.CURRICULUM_QA_STEP1_ASK_QUESTIONS,
    ]
    code_oriented_tasks = [tasks.ACTION, tasks.CURRICULUM_TASK_DECOMPOSITION]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        """
        Retrieve relevant documents based on the query.

        This function is designed to handle a wide range of tasks, including simple tasks that can
        be solved without code context, and more complex ones that require document retrieval.
        """

        # Critic tasks are preferably solvable by adding new examples in the critic.txt prompt.
        # Skill tasks are generally simple to solve as they involve wring a definition of the function created during the action phase.
        # Curriculum tasks could potentially use the crafted database to search for previous tasks which were performed at early stages during other runs.
        # CURRICULUM_QA_STEP2_ANSWER_QUESTIONS could potentially use the vector database as well to infer how to respond to questions given a task.
        # CURRICULUM_TASK_DECOMPOSTION makes use of code reitrieval to answer the question.
        if self.query_type in self.simple_tasks:
            return []

        if self.query_type in self.code_oriented_tasks:
            return self.get_documents(query, run_manager)

    def get_documents(self, query, run_manager):
        task = self.get_task(query)

        # This method now calls the internal method that performs the actual retrieval
        documents = self.base_retriever._get_relevant_documents(
            query=task, run_manager=run_manager
        )

        return documents

    def get_task(self, query):
        """
        Extracts task description from a given query string.
        """

        pattern = r"Task:.*\n" if self.query_type == tasks.ACTION else r"Final task:.*"
        match = re.search(pattern, query)
        if match:
            extracted_text = (
                match.group()[6:]
                if self.query_type == tasks.ACTION
                else match.group()[12:]
            )

        assert len(extracted_text) > 2
        return extracted_text

    @staticmethod
    def _split_documents(
        chunk_size: int,
        separators: array,
        knowledge_base: List[LangchainDocument],
        tokenizer_name: Optional[str],
    ) -> List[LangchainDocument]:
        """
        Split documents into chunks of maximum size `chunk_size` tokens and return a list of documents.
        """

        tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)

        print(f"Debug: given separators{separators}")
        text_splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
            tokenizer,
            chunk_size=chunk_size,
            chunk_overlap=int(chunk_size / 10),
            add_start_index=True,
            strip_whitespace=True,
            separators=separators,
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
