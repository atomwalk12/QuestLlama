import os

def fetch_credentials():
    azure_login = {
        "client_id": os.environ['ql_client_id'],
        "redirect_url": os.environ['ql_redirect_url'],
        "secret_value": os.environ['ql_secret_value'],
        "version": os.environ['ql_version'],
    }
    openai_api_key = os.getenv("ql_openai_api")
    
    return azure_login, openai_api_key
