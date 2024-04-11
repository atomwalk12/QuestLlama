from .code_retriever import CodeRetriever, get_base_retriever


class RetrieverFactory:
    @staticmethod
    def create_retriever(retriever_type, query_type):
        if retriever_type == "code_search":
            return RetrieverFactory._get_code_retriever(query_type=query_type)
        else:
            raise Exception(f"Retriever type {retriever_type} not recognised.")

    @staticmethod
    def _get_code_retriever(query_type):
        base_retriever, KNOWLEDGE_VECTOR_DATABASE = get_base_retriever()
        return CodeRetriever(
            query_type=query_type,
            base_retriever=base_retriever,
            knowledge_index=KNOWLEDGE_VECTOR_DATABASE,
        )
