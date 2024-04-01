# Whether to enable the questllama experiment
USE_QUESTLLAMA = True

# Can be 'gpt-4', 'gpt-3.5-turbo' or 'deepseek-coder:33b-instruct-q5_K_M'. See ollama list for other models.
MODEL = "gpt-4"

# The prompts are stored inside questllama under the directory defined below.
PROMPTS_LOCATION = "logs/prompts"

# LLM context length
CONTEXT_SIZE = 16384

# RAG configuration variables
# RAG Tokenizer: needs to be adjusted according to the local model which is used
TOKENIZER = "deepseek-ai/deepseek-coder-33b-instruct"

# RAG skill library path
SKILL_PATH = "skill_library"
DB_DIR = "./chroma_db"
K = 4
SEARCH_TYPE = "similarity"
