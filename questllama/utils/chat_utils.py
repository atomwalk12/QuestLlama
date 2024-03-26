
from langchain_community.chat_models import ChatOpenAI
from config import run_questllama
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.manager import CallbackManager


def get_chat_client(model_name, temperature=0.0, request_timeout=120):
    if run_questllama:
        return ChatOpenAI(
            base_url='http://localhost:11434/v1/',
            temperature=temperature,
            request_timeout=request_timeout,
            model_name=model_name,
            streaming=True,
            callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
        )
    else:
        return ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            request_timeout=request_timeout,
        )
