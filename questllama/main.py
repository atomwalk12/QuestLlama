from langchain import PromptTemplate, LLMChain
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser
from langchain.text_splitter import RecursiveCharacterTextSplitter, Language
from langchain.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.llms import LlamaCpp
from langchain import PromptTemplate, LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain import hub
import os



# Define constants and paths
n_gpu_layers = 25
n_batch = 1024
repo_path = "/home/razvan/Documents/thesis/Voyager"
output_path = "./output.txt"
prompt = hub.pull("rlm/rag-prompt")

# Create a loader object to load the documents from the repository
loader = GenericLoader.from_filesystem(
    repo_path,
    glob="**/*",
    suffixes=[".py"],
    parser=LanguageParser(Language.PYTHON, parser_threshold=500)
)

# Split documents into chunks and create a vector store from them
python_splitter = RecursiveCharacterTextSplitter.from_language(Language.PYTHON, chunk_size=200, chunk_overlap=200)
documents = loader.load()
texts = python_splitter.split_documents(documents)
vector_store = Chroma.from_documents(texts, HuggingFaceEmbeddings())

# Initialize a callback manager to log progress and handle events during training
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

# Create an Llama instance with the parameters specified in the question
llm = LlamaCpp(
    model_path="./Voyager/questllama/models/codellama-70b-instruct.Q5_K_M.gguf",
    n_ctx=5000,
    max_tokens=500,
    n_gpu_layers=n_gpu_layers,
    n_batch=n_batch,
    f16_kv=True,
    callback_manager=callback_manager,
    verbose=True
)

def load_qa_chain(llm: LlamaCpp, prompt):
    conversation_memory = ConversationSummaryMemory()
    
    return LLMChain(
        llm=llm, 
        memory=conversation_memory, 
        template=PromptTemplate.from_pretrained(prompt),
        retriever=vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 8}),
        chain_type="question-answering",
    )

# Get the question and document prompt
def run_chain():
    # Get user input for question and documents
    question = "How can I parse an ai message?"
    docs = vector_store.get_relevant_documents(question)
    
    # Run the chain
    result = load_qa_chain(llm, prompt).run({"input_documents": docs, "question": question})
    print("Answer:", result["output"])


def generate_fibonaci():

    # Create a chain for fibonacci generation
    fib_chain = LLMChain(llm=llm, memory=ConversationSummaryMemory(), template="Fibonacci number {n} is:")
    
    # Generate the first 10 numbers in the sequence
    for i in range(10):
        result = fib_chain.run({"n": i})
        print("Fibonacci number", i, ":", result["output"])


if __name__ == '__main__':
    generate_fibonaci()



