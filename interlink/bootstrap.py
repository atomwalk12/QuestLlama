import shared.config as Config
from questllama.extensions.chat_interaction_provider import QuestllamaClientProvider
from _voyager.extensions.chat_provider import VoyagerChatProvider


def get_client(model_name, temperature, request_timeout):
    """
    Fetches the client according to USE_QUESTLLAMA value in Config.
    If it's True, returns a QuestllamaClientProvider instance; otherwise,
    returns a VoyagerClientProvider instance.

    :return: Client Provider Instance (Questllama or Voyager)
    """
    client = (
        QuestllamaClientProvider(model_name, temperature, request_timeout)
        if Config.USE_QUESTLLAMA
        else VoyagerChatProvider(model_name, temperature, request_timeout)
    )

    return client


