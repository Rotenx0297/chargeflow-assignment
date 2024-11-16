import os
import json
import boto3

sqs = boto3.client('sqs')
eventbridge = boto3.client('events')

def lambda_handler(event, context):
    body = json.loads(event['body'])
    order_id = body.get('order_id')
    customer_name = body.get('customer_name')
    items = body.get('items')

    if order_id and customer_name and items:
        # Send valid order to SQS
        sqs.send_message(
            QueueUrl=os.environ['VALID_ORDER_QUEUE'],
            MessageBody=json.dumps(body)
        )
        # Publish validated event to EventBridge
        eventbridge.put_events(
            Entries=[
                {
                    'Source': 'com.ordersystem.order',
                    'DetailType': 'OrderValidated',
                    'Detail': json.dumps({'order_id': order_id}),
                    'EventBusName': os.environ['EVENT_BUS_NAME']
                }
            ]
        )
        return {"statusCode": 200, "body": "Order valid"}
    else:
        # Log invalid order to DLQ
        sqs.send_message(
            QueueUrl=os.environ['INVALID_ORDER_DLQ'],
            MessageBody=json.dumps({'error': 'Invalid order', 'details': body})
        )
        return {"statusCode": 400, "body": "Invalid order"}