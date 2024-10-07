import os

from aws_cdk import Stack, Duration, CfnOutput
from aws_cdk.aws_lambda import (
    DockerImageCode,
    DockerImageFunction,
    FunctionUrlAuthType,
    HttpMethod,
    FunctionUrlCorsOptions,
)
from constructs import Construct


class ResourceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Environment variables
        openai_api_key = os.getenv("OPENAI_API_KEY")
        langchain_tracing_v2 = os.getenv("LANGCHAIN_TRACING_V2")
        langchain_endpoint = os.getenv("LANGCHAIN_ENDPOINT")
        langchain_api_key = os.getenv("LANGCHAIN_API_KEY")
        langchain_project = os.getenv("LANGCHAIN_PROJECT")

        docker_function = DockerImageFunction(
            self,
            "DockerFunc",
            code=DockerImageCode.from_image_asset(
                ".",  # Point to the root, where the Dockerfile is located
                build_args={
                    "OPENAI_API_KEY": openai_api_key,
                    "LANGCHAIN_TRACING_V2": langchain_tracing_v2,
                    "LANGCHAIN_ENDPOINT": langchain_endpoint,
                    "LANGCHAIN_API_KEY": langchain_api_key,
                    "LANGCHAIN_PROJECT": langchain_project,
                },
            ),
            memory_size=1024,
            timeout=Duration.seconds(10),
        )

        function_url = docker_function.add_function_url(
            auth_type=FunctionUrlAuthType.NONE,
            cors=FunctionUrlCorsOptions(
                allowed_methods=[HttpMethod.ALL],
                allowed_headers=["*"],
                allowed_origins=["*"],
            ),
        )

        CfnOutput(self, "FunctionUrlValue", value=function_url.url)
