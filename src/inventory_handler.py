import os
import json
import boto3
import random

dynamodb = boto3.resource('dynamodb')
eventbridge = boto3.client('events')

def lambda_handler(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    for record in event['Records']:
        body = json.loads(record['body'])
        order_id = body['OrderId']
        items = body['Items']
        
        inventory_available = all(random.choice([True, False]) for _ in items)

        if inventory_available:
            table.update_item(
                Key={'OrderId': order_id},
                UpdateExpression="SET OrderStatus = :status",
                ExpressionAttributeValues={':status': 'IN_PROCESS'}
            )
            eventbridge.put_events(
                Entries=[
                    {'Source': 'com.ordersystem.order', 'DetailType': 'InventorySuccess', 'Detail': json.dumps({'OrderId': order_id})}
                ]
            )
        else:
            print(f"Inventory unavailable for {order_id}")