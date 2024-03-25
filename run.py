from questllama import QuestLlama
import os
from questllama.secret import azure_login

def run():
    voyager = QuestLlama(
        azure_login=azure_login
    )


if __name__ == "__main__":
    run()