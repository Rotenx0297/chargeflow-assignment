import os
import json
import boto3

sqs = boto3.client('sqs')
eventbridge = boto3.client('events')

def lambda_handler(event, context):
    print(event)
    body = event['detail']
    order_id = body.get('OrderId')
    customer_name = body.get('CustomerName')
    items = body.get('Items')
    print(f"Order ID: {order_id}, Customer: {customer_name}, Items: {items}")

    if order_id and customer_name and items:
        # Send valid order to SQS
        sqs.send_message(
            QueueUrl=os.environ['VALID_ORDER_QUEUE'],
            MessageBody=json.dumps(body)
        )
        print(f"Order ID: {order_id} was sent to validation sqs with content: {body}")
        # Publish validated event to EventBridge
        eventbridge.put_events(
            Entries=[
                {
                    'Source': 'com.ordersystem.order',
                    'DetailType': 'OrderValidated',
                    'Detail': json.dumps({'OrderId': order_id}),
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