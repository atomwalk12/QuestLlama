from shared.client import BaseChatProvider
from langchain_community.chat_models.openai import ChatOpenAI

from shared.messages import VoyagerMessage


class VoyagerChatProvider(BaseChatProvider):
    """A client provider for Voyager. This class allows you to get a ChatOpenAI client."""

    def __init__(self, model_name, temperature, request_timeout):
        super().__init__(
            model_name=model_name,
            temperature=temperature,
            request_timeout=request_timeout,
        )

        self.client = self._get_client(model_name, temperature, request_timeout)


    def generate(self, messages):
        """Generate messages using the LLM. As backend it defaults to the Chat-gpt API."""
        answer = self.client(messages)
        return VoyagerMessage(answer)


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

        return ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            request_timeout=request_timeout,
            # base_url="http://localhost:11434/v1/",
            # streaming=True,
            # callback_manager=callbacks
        )
