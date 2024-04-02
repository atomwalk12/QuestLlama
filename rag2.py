# Hypothetical base class
import questllama.core.utils.file_utils as U
import os
from questllama.extensions.client_provider import QuestllamaClientProvider
from langchain.schema import HumanMessage, SystemMessage



if __name__ == "__main__":
    os.environ["OPENAI_API_KEY"] = "sk-..."
    
    # Prompt
    while True:
        task_type = 'action'
        # i.e. Mine 1 wood log
        task = input("\nQuery: ")
        if task == "exit":
            break
        if task.strip() == "":
            continue

        # Prompt
        template = U.debug_load_prompt(task_type + "/system.txt")
        user = U.debug_load_prompt(task_type + "/user.txt")
        user = user.format(task=task)

        
        chat = QuestllamaClientProvider()
        msg = chat.generate(
            [
                SystemMessage(content=template),
                HumanMessage(content=user),
            ],
            task_type
        )
        print("Answer: ", msg.answer)
