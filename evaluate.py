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
    # First instantiate Voyager with skill_library_dir.
    voyager = Voyager(
        chat_provider=chat_provider_class,
        azure_login=azure_login,
        openai_api_key=openai_api_key,
        skill_library_dir="questllama/skill_library/trial1/",  # Load a learned skill library.
        ckpt_dir="runs/diamond_pickaxe2",  # Feel free to use a new dir. Do not use the same dir as skill library because new events will still be recorded to ckpt_dir.
        resume=False,  # Do not resume from a skill library because this is not learning.
    )

    # Run task decomposition
    task = "Mine 1 wood log."
    sub_goals = voyager.decompose_task(task=task)

    voyager.inference(sub_goals=sub_goals)
