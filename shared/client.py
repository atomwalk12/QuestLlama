from abc import ABC, abstractmethod


class BaseChatProvider(ABC):
    """Abstract base class for client providers.

    This class defines a common interface for all client providers to implement.
    It is meant to provide a way of retrieving clients, which are objects that perform operations on some sort of service or resource.

    Attributes:
        None
    """

    def __init__(self, model_name, temperature, request_timeout):
        self.model_name = model_name
        self.temperature = temperature
        self.request_timeout = request_timeout

    @abstractmethod
    def _get_client(self, model_name, temperature=0.0, request_timeout=120) -> object:
        """Retrieves the requested model with specified parameters.

        Args:
            model_name (str): The name of the requested model.
            temperature (float, optional): The desired temperature for the operation. Defaults to 0.0.
            request_timeout (int, optional): Timeout period for the request. Defaults to 120 seconds.

        Returns:
            object: The retrieved model or None if not found.

        """
        pass


    @abstractmethod
    def generate(self, messages):
        """
        It's responsible for generating messages using a LLM.
        """
        pass
