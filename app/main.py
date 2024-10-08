import time
import uuid
from operator import itemgetter

import boto3
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_pinecone import PineconeVectorStore

from app.configs.load_env_from_parameter_store import load_env_from_parameter_store
from app.utils.logger_util import LoggerUtil
from app.utils.vector_store.embedding_util import EmbeddingUtil

# Initialize logger
logger = LoggerUtil.get_logger()


def run(input_message):
    # LLM
    llm = ChatOpenAI(model_name="gpt-4o-mini")

    # RAG
    index_name = "about-me-index"
    embedding = EmbeddingUtil.get_embedding()
    vectorstore = PineconeVectorStore(index_name=index_name, embedding=embedding)
    retriever = vectorstore.as_retriever()

    # Prompt template
    template = """
        You are my intelligent persona, and I am currently looking for a job in Australia.
        Your role is to answer questions on my behalf, which may include topics about my personal background, 
        hobbies, professional skills, lifestyle, and work situation. Please make sure to answer all questions in 
        the first person, as if you are me.

        You can only use the information I provide here to form your responses, and you must not make anything up. 
        This is my information:
        {context}

        Here is the question:
        {question}

        Important: If the question is not related to my personal information, or if the answer is not available
        from the information I have provided, respond with "Sorry, I cannot answer that question. Perhaps you can 
        try asking something else."
    """

    prompt = ChatPromptTemplate.from_template(template)

    # Build chain
    chain = (
        {
            "context": itemgetter("question") | retriever,
            "question": itemgetter("question"),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    res = chain.invoke({"question": input_message})

    return res


def record_input_message(input_message):
    """Records the input_message with a unique ID and timestamp to DynamoDB."""
    try:
        # Initialize DynamoDB client
        dynamodb = boto3.resource("dynamodb")
        table_name = "my-website-backend-input-messages-table"
        table = dynamodb.Table(table_name)

        message_id = str(uuid.uuid4())  # Generate a unique ID for the message
        timestamp = int(time.time())  # Current timestamp in seconds

        # Store the message in DynamoDB
        table.put_item(
            Item={
                "message_id ": message_id,
                "input_message": input_message,
                "timestamp": timestamp,
            }
        )
        logger.info(f"Input message recorded with ID: {message_id}")
    except Exception as e:
        logger.error(f"Failed to record input message: {e}")
        raise


def lambda_handler(event, context):
    # Log the start of the Lambda invocation with input event and timestamp
    start_time = time.time()
    logger.info(
        f"Lambda invoked at {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(start_time))}"
    )
    logger.info(f"Input event: {event}")

    # Load environment variables from AWS Parameter Store
    load_env_from_parameter_store()

    input_message = event["input_message"]

    record_input_message(input_message)

    # Invoke the model and measure the time taken
    try:
        response_start_time = time.time()
        res = run(input_message)
        response_end_time = time.time()

        # Log response details and time taken
        logger.info(
            f"Response received in {response_end_time - response_start_time:.2f} seconds"
        )
        logger.info(f"Response content: {res}")

        # Prepare the return response
        response = {"statusCode": 200, "body": res}

    except Exception as e:
        # Log any errors during the model invocation
        logger.error(f"Error invoking model: {e}")
        response = {"statusCode": 500, "body": str(e)}

    # Log the end time and total duration of the Lambda function
    end_time = time.time()
    total_duration = end_time - start_time
    logger.info(
        f"Lambda finished at {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(end_time))}"
    )
    logger.info(f"Total execution time: {total_duration:.2f} seconds")

    return response
