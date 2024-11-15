import os
import json
import boto3

sns = boto3.client('sns')

def lambda_handler(event, context):
    for record in event['Records']:
        detail = record['detail']
        order_id = detail['order_id']
        status = detail['status']

        sns.publish(
            TopicArn=os.environ['SNS_TOPIC_ARN'],
            Message=f"Your order {order_id} is now {status}.",
            Subject=f"Order {order_id} Update"
        )