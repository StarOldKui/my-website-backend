from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI

from app.configs.load_env_from_parameter_store import load_env_from_parameter_store
from app.utils.logger_util import LoggerUtil

load_env_from_parameter_store()

logger = LoggerUtil.get_logger()


def lambda_handler(event, context):
    model = ChatOpenAI(model="gpt-4o-mini")

    messages = [
        SystemMessage(content="Translate the following from into English"),
        HumanMessage(content="你好X"),
    ]

    res = model.invoke(messages)

    return {
        'statusCode': 200,
        'body': res.content
    }


# if __name__ == '__main__':
#     print(lambda_handler(None, None))
