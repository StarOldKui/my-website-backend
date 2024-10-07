#!/usr/bin/env python3

import aws_cdk as cdk

from cdk.codepipeline_stack import CodePipelineStack

app = cdk.App()

CodePipelineStack(
    app,
    "CodePipelineStack",
    env=cdk.Environment(account="328092891197", region="us-east-2")
)

app.synth()
