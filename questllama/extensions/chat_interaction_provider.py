from langchain.schema import HumanMessage, SystemMessage
from questllama.core.retrievers.retriever_factory import CodeRetriever
from questllama.core.utils.llm_event_handler import LoggerCallbackHandler
import shared.file_utils as U
import shared.config as C
from shared import BaseChatProvider
from shared.messages import QuestllamaMessage
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
)
from typing import List, Union
import questllama.core.constants as tasks
from langchain_openai import ChatOpenAI


class QuestllamaClientProvider(BaseChatProvider):
    """A client provider for Voyager. This class allows you to get a ChatOpenAI client."""

    tasks_simple = [
        tasks.CRITIC,
        tasks.SKILL,
        tasks.CURRICULUM,
        tasks.CURRICULUM_QA_STEP2_ANSWER_QUESTIONS,
        tasks.CURRICULUM_QA_STEP1_ASK_QUESTIONS,
    ]
    tasks_require_rag = [tasks.ACTION, tasks.CURRICULUM_TASK_DECOMPOSITION]

    base_retriever = None
    logger_callback_added = False

    def __init__(self, model_name="gpt-4", temperature=0.0, request_timeout=240):
        super().__init__(
            model_name=model_name,
            temperature=temperature,
            request_timeout=request_timeout,
        )
        # Parameters
        chunk_size = 128  # maximum size
        embeddings = "flax-sentence-embeddings/st-codesearch-distilroberta-base"
        reranker = "colbert-ir/colbertv2.0"
        # Create the code retriever
        self.retriever = CodeRetriever(chunk_size, embeddings, reranker)

        # Model is used for reranking during answer_with_rag
        self.llm = self._get_client(model_name, temperature, request_timeout)

    def generate(
        self, messages: List[Union[SystemMessage, HumanMessage]], query_type: str
    ) -> QuestllamaMessage:
        """Generate messages using the LLM. As backend it defaults to Ollama."""
        self.validate_messages(messages)
        messages = self.apply_smart_replacements(messages)
        prompt_template = self.create_prompt_template(messages)

        self.llm.callbacks = []
        self.llm.callbacks += [LoggerCallbackHandler(query_type)]

        if query_type in self.tasks_require_rag:
            # Initialise RAG parameters
            rerank = True
            num_retrieved_docs = 15
            num_docs_final = 3
            knowledge_index = (
                self.retriever.knowledge_index
            )  # make it clear that knowledge_index is required

            task = self.retriever.get_task(query_type, prompt_template)

            # Answer to the task. Load reranker separately.
            answer, docs = CodeRetriever.answer_with_rag(
                task,
                prompt_template,
                self.llm,
                knowledge_index,
                reranker=self.retriever.reranker if rerank else None,
                num_retrieved_docs=num_retrieved_docs,
                num_docs_final=num_docs_final,
            )
            return QuestllamaMessage(answer.content)
        else:
            # Answer without retrieving rag documents
            answer = self.llm.invoke(prompt_template.format())
            return QuestllamaMessage(answer.content)

    def validate_messages(self, messages: List[Union[SystemMessage, HumanMessage]]):
        assert isinstance(
            messages[0], SystemMessage
        ), "First message must be a SystemMessage"
        for message in messages[1:]:
            assert isinstance(
                message, HumanMessage
            ), "Following messages must be HumanMessages"

    def apply_smart_replacements(
        self, messages: List[Union[SystemMessage, HumanMessage]]
    ) -> List[Union[SystemMessage, HumanMessage]]:
        for message in messages:
            message.content = U.smart_replace_braces(message.content)
        return messages

    def create_prompt_template(
        self, messages: List[Union[SystemMessage, HumanMessage]]
    ):
        return ChatPromptTemplate.from_messages(
            [SystemMessagePromptTemplate.from_template(messages[0].content)]
            + messages[1:]
        )

    def _get_client(self, model_name="gpt-4", temperature=0.0, request_timeout=120):
        """
        Returns a new instance of the Ollama client with the provided parameters.
        The handle is used to redirect output to stdout during the output generation.
        """

        return ChatOpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama",  # required, but unused
            temperature=temperature,
            streaming=True,
            callbacks=[],
            request_timeout=request_timeout,
            model=C.MODEL,
        )
