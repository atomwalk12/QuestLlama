import os


def fetch_credentials():
    """
    Fetches credentials from environment variables.

    :return: azure_login (dict), openai_api_key (str)
    """
    azure_login = {
        "client_id": os.getenv("ql_client_id"),
        "redirect_url": os.getenv("ql_redirect_url"),
        "secret_value": os.getenv("ql_secret_value"),
        "version": os.getenv("ql_version"),
    }

    openai_api_key = os.getenv("ql_openai_api")

    return azure_login, openai_api_key
