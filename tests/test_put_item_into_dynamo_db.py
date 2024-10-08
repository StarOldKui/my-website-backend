import boto3
import uuid
import time

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("my-website-backend-input-messages-table")

message_id = str(uuid.uuid4())
input_message = "Test input message"
timestamp = int(time.time())

response = table.put_item(
    Item={
        "message_id": message_id,
        "input_message": input_message,
        "timestamp": timestamp
    }
)

print("PutItem succeeded:", response)
