from questllama import QuestLlama
from voyager import Voyager
import os


azure_login = {
    "client_id": os.environ['ql_client_id'],
    "redirect_url": os.environ['ql_redirect_url'],
    "secret_value": os.environ['ql_secret_value'],
    "version": os.environ['ql_version'],
}
openai_api_key = os.getenv("qs_openai_api_key")


voyager = Voyager(
        azure_login=azure_login,
        openai_api_key=openai_api_key,
    )

voyager.learn(reset_env=False)
