import os
import json
import boto3

dynamodb = boto3.resource('dynamodb')
eventbridge = boto3.client('events')

def lambda_handler(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    print(event)
    body = event['detail']
    print(body)
    order_id = body['OrderId']

    table.update_item(
        Key={'OrderId': order_id},
        UpdateExpression="SET OrderStatus = :status",
        ExpressionAttributeValues={':status': 'COMPLETED'}
    )
    # Log valid processing to EventBridge
    eventbridge.put_events(
        Entries=[
            {'Source': 'com.ordersystem.order', 'DetailType': 'OrderCompleted', 'Detail': json.dumps(body), 'EventBusName': os.environ['EVENT_BUS_NAME']}
        ]
    )