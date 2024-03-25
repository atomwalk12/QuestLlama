from time import sleep
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from voyager import Voyager
import questllama.utils as U
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.manager import CallbackManager


def query_instruct(system_message, human_message):
    llm = ChatOllama(model="codellama:70b-instruct-q5_K_M_local", num_ctx=4096, stop=["Source:", "Destination:", "<step>"], temperature=0.0,
                    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))
    llm([system_message, human_message])


def query_70b_code(system_message, human_message):
    llm = ChatOllama(model="codellama:70b-code-q5_K_M", num_ctx=16384, temperature=0.0,
                    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))
    llm([system_message, human_message])

def query_7b_code(system_message, human_message):
    llm = ChatOllama(model="codellama:7b", num_ctx=16384, temperature=0.0,
                    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))
    llm([system_message, human_message])


def query_34b_code(system_message, human_message):
    llm = ChatOllama(model="codellama:34b-code-q4_K_M", num_ctx=4000, temperature=0.5,
                    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))
    llm([system_message, human_message])


class QuestLlama():
    def __init__(self, azure_login, base_url='http://localhost:11434/api/generate'):
        # super().__init__(azure_login=azure_login, openai_api_key='not-needed', openai_api_request_timeout=600)
        system = U.load_text('system_message.txt')
        user = U.load_text('human_message.txt')
        system_message = SystemMessage(content=system)

        human_message = HumanMessage(content=user)

        query_instruct(system_message, human_message)

