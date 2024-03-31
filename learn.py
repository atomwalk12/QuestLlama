from questllama import fetch_credentials
from questllama.extensions.client_provider import QuestllamaClientProvider
from shared.config import USE_QUESTLLAMA
from voyager.core.client_provider import VoyagerClientProvider
from voyager import Voyager

# Get login credentials and launch the experiment.
azure_login, openai_api_key = fetch_credentials()

# Determine which client provider to use based on configuration
client_provider_class = QuestllamaClientProvider if USE_QUESTLLAMA else VoyagerClientProvider


# Inject this class into the factory function
client = Voyager(client_provider=client_provider_class, model_name="model", temperature=0.5, request_timeout=100)
