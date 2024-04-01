
from abc import abstractmethod
from langchain.schema import AIMessage

class IMessageWrapper(AIMessage):

    @property
    @abstractmethod
    def answer(self):
        pass


class QuestllamaMessage(IMessageWrapper):


    def __init__(self, message, **kwargs):
        super().__init__(content=message['result'], **kwargs)
        self.message = message
    
    @property
    def answer(self):
        return self.message['result']


class VoyagerMessage(IMessageWrapper):

    def __init__(self, message, **kwargs):
        super().__init__(content=message.content, **kwargs)
        self.message = message

    @property
    def answer(self):
        return self.message.content
