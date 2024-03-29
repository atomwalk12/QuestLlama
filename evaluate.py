from questllama import QuestLlama
from voyager import Voyager
import os


azure_login = {
    "client_id": os.environ['ql_client_id'],
    "redirect_url": os.environ['ql_redirect_url'],
    "secret_value": os.environ['ql_secret_value'],
    "version": os.environ['ql_version'],
}
openai_api_key = os.getenv("ql_openai_api")


# First instantiate Voyager with skill_library_dir.
voyager = Voyager(
    azure_login=azure_login,
    openai_api_key=openai_api_key,
    skill_library_dir="/home/razvan/Documents/thesis/Voyager/skill_library/trial1/", # Load a learned skill library.
    ckpt_dir="runs/diamond_pickaxe", # Feel free to use a new dir. Do not use the same dir as skill library because new events will still be recorded to ckpt_dir. 
    resume=False # Do not resume from a skill library because this is not learning.
)

# Run task decomposition
task = "Mine 1 wood log."
sub_goals = voyager.decompose_task(task=task)

voyager.inference(sub_goals=sub_goals)

