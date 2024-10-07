#!/usr/bin/env python3

import aws_cdk as cdk

from cdk.my_website_backend_stack import MyWebsiteBackendStack

app = cdk.App()
MyWebsiteBackendStack(app, "MyWebsiteBackendStack")

app.synth()
