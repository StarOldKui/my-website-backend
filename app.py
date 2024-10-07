#!/usr/bin/env python3

import aws_cdk

from cdk.codepipeline_stack import CodePipelineStack

from app.utils.env_util import EnvLoader

EnvLoader()

app = aws_cdk.App()

CodePipelineStack(
    app,
    "CodePipelineStack",
    env=aws_cdk.Environment(account="328092891197", region="us-east-2"),
)

app.synth()
