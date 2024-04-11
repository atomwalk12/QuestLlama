# Hypothetical base class
import questllama.core.utils.file_utils as U
import os
from questllama.extensions import QuestllamaClientProvider
from langchain.schema import HumanMessage, SystemMessage

from _voyager.agents.action import ActionAgent

task = ""

if __name__ == "__main__":
    os.environ["OPENAI_API_KEY"] = "sk-..."

    # Prompt
    while True:
        task_type = "curriculum_qa_step1_ask_questions"
        # i.e. Mine 1 wood log
        task = input("\nQuery: ")
        task_type = task_type if task == "" else task
        if task == "exit":
            break

        # Prompt
        if task_type == "action":
            agent = ActionAgent()
            template = agent.render_system_message()
        else:
            template = U.debug_load_prompt(f"{task_type}.txt")
        user = U.debug_load_prompt("/debugging/" + task_type + "/user.txt")
        if task_type == "action" and user.find("{task}") != -1:
            user = user.format(task=task)

        chat = QuestllamaClientProvider()
        msg = chat.generate(
            [
                SystemMessage(
                    content=template.content
                    if isinstance(template, SystemMessage)
                    else template
                ),
                HumanMessage(content=user),
            ],
            task_type,
        )
        print("Answer: ", msg.answer)
