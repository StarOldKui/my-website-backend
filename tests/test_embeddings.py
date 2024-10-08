from langchain_core.vectorstores import InMemoryVectorStore

from app.utils.vector_store.embedding_util import EmbeddingUtil
from app.utils.env_util import EnvLoader

EnvLoader()

text = "PERSONAL BACKGROUND I am 27 years old, originally from Shenzhen, China. I have a passion for computers, music, and programming. I enjoy staying on top of new technology trends and applying them in my work."

vectorstore = InMemoryVectorStore.from_texts(
    [text],
    embedding=EmbeddingUtil.get_embedding(),
)

# Use the vectorstore as a retriever
retriever = vectorstore.as_retriever()

# Retrieve the most similar text
retrieved_documents = retriever.invoke("Who am I?")

# show the retrieved document's content
print(retrieved_documents[0].page_content)
