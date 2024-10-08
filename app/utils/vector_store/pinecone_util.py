import os

from pinecone import Pinecone, PodSpec

from app.utils.logger_util import LoggerUtil

logger = LoggerUtil.get_logger()


class PineconeUtil:
    _pc: Pinecone = None

    @staticmethod
    def _initialize():
        pinecone_api_key = os.getenv("PINECONE_API_KEY")
        PineconeUtil._pc = Pinecone(api_key=pinecone_api_key)

    @staticmethod
    def get_pc():
        if not PineconeUtil._pc:
            PineconeUtil._initialize()
        return PineconeUtil._pc

    @staticmethod
    def create_index(index_name: str, dimension: int = 1536, metric: str = "cosine"):
        """
        Creates a Pinecone index if it doesn't already exist.

        Args:
            index_name (str): The name of the Pinecone index to create.
            dimension (int): The dimensionality of the vectors to be stored in the index. Default is 1536 for text-embedding-3-small.
            metric (str): The metric used to calculate similarity between vectors. Default is "cosine".

        The function checks if the specified index already exists. If not, it creates a new index
        with the given parameters. It logs information about the operation and handles exceptions
        gracefully.
        """
        try:
            pc = PineconeUtil.get_pc()

            # Check if index already exists
            existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]
            if index_name in existing_indexes:
                logger.info(f"Index '{index_name}' already exists.")
                return

            # Create a new index
            pc.create_index(
                name=index_name,
                dimension=dimension,
                metric=metric,
                spec=PodSpec(environment="gcp-starter"),
            )

            logger.info(f"Successfully created the index: {index_name}")
        except Exception as e:
            logger.error(
                f"Failed to create or access the index '{index_name}'. Error: {e}"
            )

    @staticmethod
    def _chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i : i + n]
