# Built-in modules and third-party libraries
from langchain_community.chat_models import ChatOpenAI
from langchain.callbacks.manager import CallbackManager

from shared.client import BaseChatProvider
from questllama.core.utils import LoggerCallbackHandler


class QuestllamaClientProvider(BaseChatProvider):
    """A client provider for Voyager. This class allows you to get a ChatOpenAI client."""

    logger_callback_added = False

    def __init__(self, model_name, temperature, request_timeout):
        super().__init__(
            model_name=model_name,
            temperature=temperature,
            request_timeout=request_timeout,
        )

        self.client = self._get_client(model_name, temperature, request_timeout)

    def generate():
        """Generate messages using the LLM. As backend it defaults to Ollama."""
        


    def _get_client(self, model_name, temperature=0.0, request_timeout=120):
        """
        Returns a new instance of the ChatOpenAI client with the provided parameters.

        Parameters:
            model_name (str): The name of the model to use for this client.
            temperature (float, optional): The temperature to use when generating responses. Defaults to 0.0.
            request_timeout (int, optional): The timeout for requests in seconds. Defaults to 120.

        Returns:
            ChatOpenAI: A new instance of the ChatOpenAI client with the provided parameters.
        """
        callbacks = CallbackManager([])

        # Add LoggerCallbackHandler only if it hasn't been added before
        if not self.logger_callback_added:
            callbacks.add_handler(LoggerCallbackHandler())
            self.logger_callback_added = (
                True  # Mark as added in order to write data only once
            )

        return ChatOpenAI(
            base_url="http://localhost:11434/v1/",
            temperature=temperature,
            request_timeout=request_timeout,
            model_name=model_name,
            streaming=True,
            callback_manager=callbacks,
        )
