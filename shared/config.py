# Whether to enable the questllama experiment
USE_QUESTLLAMA = True

# Can be 'gpt-4', 'gpt-3.5-turbo' or 'deepseek-coder:33b-instruct-q5_K_M'. See ollama list for other models.
MODEL = "gpt-4"

# The prompts are stored inside questllama under the directory defined below.
PROMPTS_LOCATION = "logs/prompts"

# LLM context length
CONTEXT_SIZE = 16384