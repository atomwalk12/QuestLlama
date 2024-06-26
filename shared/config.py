from langchain_community.embeddings import GPT4AllEmbeddings

# Whether to enable the questllama experiment
USE_QUESTLLAMA = True

# Can be 'gpt-4', 'gpt-3.5-turbo' or 'deepseek-coder:33b-instruct-q5_K_M'. See ollama list for other models.
MODEL = "llama3:70b-instruct"

# The prompts are stored inside questllama under the directory defined below.
PROMPTS_LOCATION = "logs/prompts"

# LLM context length
# CONTEXT_SIZE = 16384
CONTEXT_SIZE = 8192

# RAG configuration variables
# RAG Tokenizer: needs to be adjusted according to the local model which is used
# TOKENIZER = "deepseek-ai/deepseek-coder-33b-instruct"
TOKENIZER = "meta-llama/Meta-Llama-3-70B-Instruct"

# RAG skill library path
SKILL_PATH = "skill_library"
DB_DIR = "./faiss_db"
K = 5
SEARCH_TYPE = "similarity"
EMBEDDING = GPT4AllEmbeddings
CHUNK_OVERLAP = 100
CHUNK_SIZE = 800
RETRIEVER = "unused"  # 'hybrid' or 'simple'
