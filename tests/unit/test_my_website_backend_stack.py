import aws_cdk as core
import aws_cdk.assertions as assertions

from my_website_backend.my_website_backend_stack import MyWebsiteBackendStack

# example tests. To run these tests, uncomment this file along with the example
# resource in my_website_backend/my_website_backend_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = MyWebsiteBackendStack(app, "my-website-backend")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
