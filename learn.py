from shared import fetch_credentials
from questllama.extensions.chat_interaction_provider import QuestllamaClientProvider
from shared.config import USE_QUESTLLAMA
from _voyager.extensions.chat_provider import VoyagerChatProvider
from _voyager import Voyager

if __name__ == "__main__":
    # Get login credentials and launch the experiment.
    azure_login, openai_api_key = fetch_credentials()

    # Determine which client provider to use based on configuration
    chat_provider_class = (
        QuestllamaClientProvider if USE_QUESTLLAMA else VoyagerChatProvider
    )

    # Inject this class into the factory function
    client = Voyager(
        chat_provider=chat_provider_class,
        azure_login=azure_login,
        openai_api_key=openai_api_key,
        resume=True,
        max_iterations=180,
    )

    # start lifelong learning
    client.learn()
