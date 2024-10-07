# from aws_cdk import Stack, Duration, CfnOutput
# from aws_cdk.aws_lambda import (
#     DockerImageCode,
#     DockerImageFunction,
#     FunctionUrlAuthType,
#     HttpMethod,
#     FunctionUrlCorsOptions,
# )
# from constructs import Construct
#
#
# class ResourceStack(Stack):
#
#     def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
#         super().__init__(scope, construct_id, **kwargs)
#
#         docker_function = DockerImageFunction(
#             self,
#             "DockerFunc",
#             code=DockerImageCode.from_image_asset(
#                 "."
#             ),  # Point to the root, where the Dockerfile is located
#             memory_size=1024,
#             timeout=Duration.seconds(10),
#         )
#
#         function_url = docker_function.add_function_url(
#             auth_type=FunctionUrlAuthType.NONE,
#             cors=FunctionUrlCorsOptions(
#                 allowed_methods=[HttpMethod.ALL],
#                 allowed_headers=["*"],
#                 allowed_origins=["*"],
#             ),
#         )
#
#         CfnOutput(self, "FunctionUrlValue", value=function_url.url)
