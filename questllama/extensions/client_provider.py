from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.llms import Ollama
from langchain.schema import HumanMessage, SystemMessage
import questllama.core.utils.file_utils as U
import questllama.core.utils.log_utils as L
from shared import BaseChatProvider
from shared.messages import QuestllamaMessage
from questllama.extensions.rag import RetrievelSearchModels


class QuestllamaClientProvider(BaseChatProvider):
    """A client provider for Voyager. This class allows you to get a ChatOpenAI client."""

    base_retriever = None
    logger_callback_added = False

    def __init__(self, model_name="gpt-4", temperature=0.0, request_timeout=240):
        super().__init__(
            model_name=model_name,
            temperature=temperature,
            request_timeout=request_timeout,
        )
        self.models = RetrievelSearchModels(skill_library='skill_library')

        self.client = self._get_client(model_name, temperature, request_timeout)


    def generate(self, messages, query_type):
        """Generate messages using the LLM. As backend it defaults to Ollama."""
        assert len(messages) <= 2
        assert isinstance(messages[0], SystemMessage)
        assert isinstance(messages[1], HumanMessage)

        retriever = self.models.get_retriever(query_type=query_type)

        QA_CHAIN_PROMPT = PromptTemplate(
            input_variables=["context", "question"],
            template=messages[0].content,  # system prompt
        )

        qa_chain = RetrievalQA.from_chain_type(
            self.client,
            retriever=retriever,
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
            return_source_documents=True,
        )

        self.result = qa_chain(
            {"query": messages[1].content}, callbacks=[L.LoggerCallbackHandler()]
        )  # user prompt

        return QuestllamaMessage(self.result)

    def _get_client(self, model_name="gpt-4", temperature=0.0, request_timeout=120):
        """
        Returns a new instance of the Ollama client with the provided parameters.
        The handle is used to redirect output to stdout during the output generation.
        """

        return Ollama(
            temperature=temperature, model=model_name, timeout=request_timeout
        )
