import os
import json
import boto3
import random

sqs = boto3.client('sqs')
dynamodb = boto3.resource('dynamodb')
eventbridge = boto3.client('events')

def lambda_handler(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    for record in event['Records']:
        body = json.loads(record['body'])
        order_id = body['OrderId']
        items = body['Items']
        
        inventory_available = True # For testing
        # inventory_available = all(random.choice([True, False]) for _ in items)

        if inventory_available:
            table.update_item(
                Key={'OrderId': order_id},
                UpdateExpression="SET OrderStatus = :status",
                ExpressionAttributeValues={':status': 'IN_PROCESS'}
            )
            print(f"Order ID: {order_id} was updated in DDB with status: IN_PROCESS")
            eventbridge.put_events(
                Entries=[
                    {'Source': 'com.ordersystem.order', 'DetailType': 'InventorySuccess', 'Detail': json.dumps({'OrderId': order_id}), 'EventBusName': os.environ['EVENT_BUS_NAME']}
                ]
            )
        else:
            # Log invalid processing to DLQ
            sqs.send_message(
                QueueUrl=os.environ['INVALID_ORDER_PROCESSOR_DLQ'],
                MessageBody=json.dumps({'error': 'Invalid order processing', 'details': body})
            )
            eventbridge.put_events(
                Entries=[
                    {'Source': 'com.ordersystem.order', 'DetailType': 'InventoryFailure', 'Detail': json.dumps({'OrderId': order_id}), 'EventBusName': os.environ['EVENT_BUS_NAME']}
                ]
            )
            return {"statusCode": 400, "body": "Invalid order processing"}