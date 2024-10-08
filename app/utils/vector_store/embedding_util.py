from langchain_core.embeddings.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings


class EmbeddingUtil:
    _embedding: Embeddings = None

    @staticmethod
    def _initialize():
        EmbeddingUtil._embedding = OpenAIEmbeddings(model="text-embedding-3-small")

    @staticmethod
    def get_embedding():
        if not EmbeddingUtil._embedding:
            EmbeddingUtil._initialize()
        return EmbeddingUtil._embedding
