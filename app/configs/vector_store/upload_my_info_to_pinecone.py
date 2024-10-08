from langchain_pinecone import PineconeVectorStore

from app.utils.env_util import EnvLoader
from app.utils.logger_util import LoggerUtil
from app.utils.vector_store.embedding_util import EmbeddingUtil
from app.utils.vector_store.pinecone_util import PineconeUtil

EnvLoader()

logger = LoggerUtil.get_logger()


def read_paragraphs_from_file(file_path):
    paragraphs = []
    with open(file_path, "r", encoding="utf-8") as file:
        # Read the entire file content and split by double newlines (empty line as separator)
        content = file.read()
        paragraphs = content.strip().split("\n\n")  # Split on double newlines

    return paragraphs


def upload_my_info_to_pinecone(paragraphs):
    index_name = "about-me-index"

    # Create the Pinecone index if it does not exist
    PineconeUtil.create_index(index_name)

    text_metadata_pairs = []

    for paragraph in paragraphs:
        text_for_embedding = paragraph
        metadata = {"text": text_for_embedding}
        # Append text and corresponding metadata as a tuple to the list
        text_metadata_pairs.append((text_for_embedding, metadata))

    try:
        logger.info("Start inserting...")
        batch_size = 100
        for batch in PineconeUtil._chunks(text_metadata_pairs, batch_size):
            # Extract texts and metadatas for the current batch
            texts, metadatas = zip(*batch)

            # Upload data to Pinecone
            PineconeVectorStore.from_texts(
                index_name=index_name,
                texts=list(texts),
                metadatas=list(metadatas),
                embedding=EmbeddingUtil.get_embedding(),
            )
        logger.info("Successfully embedded the texts")
    except Exception as e:
        logger.error(f"Failed to upload data to Pinecone. Error: {e}")


if __name__ == "__main__":
    file_path = "about_me.txt"
    paragraphs = read_paragraphs_from_file(file_path)
    upload_my_info_to_pinecone(paragraphs)
