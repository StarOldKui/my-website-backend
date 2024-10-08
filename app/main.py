import time

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI

from app.configs.load_env_from_parameter_store import load_env_from_parameter_store
from app.utils.logger_util import LoggerUtil

# Initialize logger
logger = LoggerUtil.get_logger()


def lambda_handler(event, context):
    # Log the start of the Lambda invocation with input event and timestamp
    start_time = time.time()
    logger.info(
        f"Lambda invoked at {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(start_time))}"
    )
    logger.info(f"Input event: {event}")

    # Load environment variables from AWS Parameter Store
    load_env_from_parameter_store()

    # Example parameters to be passed in the Lambda
    model_name = "gpt-4o-mini"
    input_message = "你好X"

    # Log parameters being used in the request
    logger.info(f"Using model: {model_name}")
    logger.info(f"Input message: {input_message}")

    # Create an OpenAI chat model and generate a response
    model = ChatOpenAI(model=model_name)

    messages = [
        SystemMessage(content="Translate the following from into English"),
        HumanMessage(content=input_message),
    ]

    # Invoke the model and measure the time taken
    try:
        response_start_time = time.time()
        res = model.invoke(messages)
        response_end_time = time.time()

        # Log response details and time taken
        logger.info(
            f"Response received in {response_end_time - response_start_time:.2f} seconds"
        )
        logger.info(f"Response content: {res.content}")

        # Prepare the return response
        response = {"statusCode": 200, "body": res.content}

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


if __name__ == '__main__':
    print(lambda_handler(None, None))
