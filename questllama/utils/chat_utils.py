from langchain_community.chat_models import ChatOpenAI
from langchain.callbacks.manager import CallbackManager

from questllama.config import run_questllama
from .logger_callback import LoggerCallbackHandler


logger_callback_added = False


def get_chat_client(model_name, temperature=0.0, request_timeout=120):
    global logger_callback_added
    callbacks = CallbackManager([])
    
    # Add LoggerCallbackHandler only if it hasn't been added before
    if not logger_callback_added:
        callbacks.add_handler(LoggerCallbackHandler())
        logger_callback_added = True  # Mark as added

    if run_questllama:
        return ChatOpenAI(
            base_url='http://localhost:11434/v1/',
            temperature=temperature,
            request_timeout=request_timeout,
            model_name=model_name,# "deepseek-coder:33b-instruct-q5_K_M",
            streaming=True,
            callback_manager=callbacks
        )
    else:
        return ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            request_timeout=request_timeout,
        )
