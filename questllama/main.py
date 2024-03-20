from langchain.text_splitter import Language
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.llms import LlamaCpp
from langchain import PromptTemplate, LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain import hub
from langchain.chains.question_answering import load_qa_chain

n_gpu_layers = 25
n_batch = 1024
repo_path = "/home/razvan/Documents/thesis/Voyager"

loader = GenericLoader.from_filesystem(
    repo_path,
    glob="**/*",
    suffixes=[".py"],
    parser=LanguageParser(Language.PYTHON, parser_threshold=500)
)

documents = loader.load()

python_splitter = RecursiveCharacterTextSplitter.from_language(Language.PYTHON, chunk_size=2000, chunk_overlap=200)

texts = python_splitter.split_documents(documents)


# Create a vector store from the documents
db = Chroma.from_documents(texts, HuggingFaceEmbeddings())
retriever = db.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 8},
)

callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
llm = LlamaCpp(
    # model_path="./Voyager/questllama/models/codellama-70b-instruct.Q5_K_M.gguf",
    model_path="./Voyager/questllama/models/codellama-70b-instruct.Q5_K_M.gguf",
    n_ctx=5000,
    max_tokens=5000,
    n_gpu_layers=n_gpu_layers,
    n_batch=n_batch,
    f16_kv=True,
    callback_manager=callback_manager,
    verbose=True
)

QA_CHAIN_PROMPT = hub.pull("rlm/rag-prompt")

# # Docs
question = "How can I parse an ai message?"
docs = retriever.get_relevant_documents(question)

# # Chain
chain = load_qa_chain(llm, chain_type="stuff", prompt=QA_CHAIN_PROMPT)

# # Run
chain({"input_documents": docs, "question": question}, return_only_outputs=True)
