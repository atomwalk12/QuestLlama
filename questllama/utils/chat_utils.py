from langchain_community.chat_models import ChatOpenAI
from langchain.callbacks.manager import CallbackManager

from questllama.config import run_questllama
from .logger_callback import LoggerCallbackHandler


def get_chat_client(model_name, temperature=0.0, request_timeout=120):
    if run_questllama:
        return ChatOpenAI(
            base_url='http://localhost:11434/v1/',
            temperature=temperature,
            request_timeout=request_timeout,
            model_name=model_name,
            streaming=True,
            callback_manager=CallbackManager([LoggerCallbackHandler()])
        )
    else:
        return ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            request_timeout=request_timeout,
        )
