import os
import json
import boto3

sns = boto3.client('sns')

def lambda_handler(event, context):
    print(event)
    status = event['detail-type']
    body = event['detail']
    print(body)
    order_id = body['OrderId']

    sns.publish(
        TopicArn=os.environ['SNS_TOPIC_ARN'],
        Message=f"Your order {order_id} is now {status}.",
        Subject=f"Order {order_id} Update"
    )
    print(f"SNS notification was sent for Order ID: {order_id}")