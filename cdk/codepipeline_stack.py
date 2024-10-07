import aws_cdk as cdk
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep
from constructs import Construct


class CodePipelineStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        git_connection = CodePipelineSource.connection(
            repo_string="StarOldKui/my-website-backend",
            branch="main",
            connection_arn="arn:aws:codestar-connections:us-east-2:328092891197:connection/7313505d-bbe4-466a-b9ea-e8eb6ca66314",
        )

        code_pipeline = CodePipeline(
            self,
            "CodePipeline",
            pipeline_name="MyWebsiteBackendPipeline",
            synth=ShellStep(
                "Synth",
                input=git_connection,
                commands=[
                    "npm install -g aws-cdk",
                    "python -m pip install -r requirements.txt",
                    "cdk synth",
                ],
            ),
        )
