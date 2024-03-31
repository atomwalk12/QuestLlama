from abc import ABC, abstractmethod

class BaseChatProvider(ABC):
    """Abstract base class for client providers.

    This class defines a common interface for all client providers to implement.
    It is meant to provide a way of retrieving clients, which are objects that perform operations on some sort of service or resource.

    Attributes:
        None
    """
  
    @abstractmethod
    def _get_client(self):
        """An abstract method for obtaining a client object.

        This function should be overridden by any class that inherits from BaseClientProvider to provide the specific behavior
        of how to retrieve a client object. The details of this behavior depend on the particular implementation, but typically it involves
        creating and configuring a new instance of some kind of client object.

        Raises:
            NotImplementedError: If this function is not overridden by a subclass.
        """
        pass
