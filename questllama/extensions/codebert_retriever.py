from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)
from langchain.docstore.document import Document as LangchainDocument
from typing import Optional, List

import questllama.core.utils.file_utils as U
import questllama.core.utils.log_utils as L
from transformers import AutoTokenizer



class CodebertRetriever:
    JAVASCRIPT_SEPARATORS = [
        "\nfunction ",
        "\nconst ",
        "\nlet ",
        "\nvar ",
        "\nclass ",
        "\nif ",
        "\nfor ",
        "\nwhile ",
        "\nswitch ",
        "\ncase ",
        "\ndefault ",
        "\n\n",
        "\n",
        " ",
        "",
    ]

    def __init__(self, skill_library):
        self.logger = L.QuestLlamaLogger("OllamaAPI")


    def read_knowledge_database(self):
        self.action_files = U.read_skill_library("skill_library", full_path=True)
        self.logger.log(
            "info",
            f"Skill Library. Read {len(self.action_files)} javascript files.",
            "chromadb",
        )
        return [
            LangchainDocument(page_content=doc[1], metadata={"source": doc[0]})
            for doc in self.action_files
        ]

    def split_documents(
        self,
        chunk_size: int,
        knowledge_base: List[LangchainDocument],
        tokenizer_name: Optional[str] = "microsoft/codebert-base",
    ) -> List[LangchainDocument]:
        """
        Split documents into chunks of maximum size `chunk_size` tokens and return a list of documents.
        """

        text_splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
            AutoTokenizer.from_pretrained(tokenizer_name),
            chunk_size=chunk_size,
            chunk_overlap=int(chunk_size / 10),
            add_start_index=True,
            strip_whitespace=True,
            separators=self.JAVASCRIPT_SEPARATORS,
        )

        docs_processed = []
        for doc in knowledge_base:
            docs_processed += text_splitter.split_documents([doc])

        # Remove duplicates
        unique_texts = {}
        docs_processed_unique = []
        for doc in docs_processed:
            if doc.page_content not in unique_texts:
                unique_texts[doc.page_content] = True
                docs_processed_unique.append(doc)

        return docs_processed_unique
