# QuestLlama

This version of Voyager uses the open-source Code Llama Instruct 70b LLM model instead of ChatGPT.

## Prerequisites

Useful area to teleport the bot to in order to start experiments: -94 89 -34
Check bot inventory: /data get entity bot Inventory


## Models currently used
ollama cp codellama-70b-instruct.Q5_K_M gpt-4
ollama cp deepseek-coder:33b-instruct-q5_K_M gpt-3.5-turbo


# Done
* Add a custom message class which correctly gets the input from the model.
* Modify old voyager to use prompts/voyager/
* Replace { with {{ for questllama prompts


# Known problems
See https://github.com/MineDojo/Voyager/issues/120
