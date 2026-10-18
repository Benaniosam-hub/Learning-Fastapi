import boto3
import json

sqs = boto3.client("sqs", region_name="us-east-1")

queue_url = "https://sqs.us-east-1.amazonaws.com/535237074578/employeeQ"

payload = {
    "username": "mel",
    "email": "mel@gmail.com",
    "first_name": "mel",
    "last_name": "rai",
    "password": "Mel@123",
    "role": "user"
}

response = sqs.send_message(
    QueueUrl = queue_url,
    MessageBody = json.dumps(payload)
)

print("Message sent successfully")
print("Message ID:", response["MessageId"])
