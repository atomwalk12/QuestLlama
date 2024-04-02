# QuestLlama: Embodied Agents in Minecraft

Check the original readme at: https://github.com/MineDojo/Voyager

# Todo
- Summarise the essential parts of the Voyager application installation process.

# QuestLlama installation
- Direct the user at the QuestLlama [README.md](questllama/README.md) file.

FIXME: write a tutorial on how to use ollama
# Install Ollama
  >> curl -fsSL https://ollama.com/install.sh | sh


# RAG
## Hybrid search using
- using keyword based search (BM25Retriever) and Ensemble Retriever (combines the two searches). The default version uses embedded based search (HugginfaceInferenceAPIEmbeddings) which is also called Semantic Search.

embeddings = HuggingFaceInferenceAPIEmbeddings(
    api_key=HF_TOKEN, model_name="BAAI/bge-base-en-v1.5"
)

vectorstore = Chroma.from_documents(chunks, embeddings)

### Semantic Search
vectorstore_retreiver = vectorstore.as_retriever(search_kwargs={"k": 3})
 

### Keyword Search
keyword_retriever = BM25Retriever.from_documents(chunks)
keyword_retriever.k =  3


### Ensemble retriever
ensemble_retriever = EnsembleRetriever(retrievers=[vectorstore_retreiver,
                                                   keyword_retriever],
                                       weights=[0.5, 0.5])
                                       