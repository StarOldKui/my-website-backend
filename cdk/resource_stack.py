from aws_cdk import Stack, Duration, CfnOutput
from aws_cdk import aws_iam as iam  # Import IAM module
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

        # Create the Lambda function using the Docker image
        docker_function = DockerImageFunction(
            self,
            "DockerFunc",
            code=DockerImageCode.from_image_asset(
                ".",  # Point to the root, where the Dockerfile is located
            ),
            memory_size=1024,
            timeout=Duration.seconds(10),
        )

        # Add permissions to allow Lambda to access Parameter Store
        docker_function.add_to_role_policy(
            iam.PolicyStatement(
                actions=["ssm:GetParameter", "ssm:GetParametersByPath"],
                resources=[
                    f"arn:aws:ssm:{self.region}:{self.account}:parameter/my-website-backend/*"
                ],
                effect=iam.Effect.ALLOW,
            )
        )

        # Add permissions to allow Lambda to access DynamoDB
        docker_function.add_to_role_policy(
            iam.PolicyStatement(
                actions=["dynamodb:PutItem"],
                resources=[
                    f"arn:aws:dynamodb:{self.region}:{self.account}:table/my-website-backend-input-messages-table"
                ],
                effect=iam.Effect.ALLOW,
            )
        )

        # Set up the Function URL with CORS
        function_url = docker_function.add_function_url(
            auth_type=FunctionUrlAuthType.NONE,
            cors=FunctionUrlCorsOptions(
                allowed_methods=[HttpMethod.ALL],
                allowed_headers=["*"],
                allowed_origins=["*"],
            ),
        )

        # Output the Function URL
        CfnOutput(self, "FunctionUrlValue", value=function_url.url)
