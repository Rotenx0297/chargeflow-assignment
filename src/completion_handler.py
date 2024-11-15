import os
import json
import boto3

dynamodb = boto3.resource('dynamodb')
eventbridge = boto3.client('events')

def lambda_handler(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    for record in event['Records']:
        detail = record['detail']
        order_id = detail['order_id']

        table.update_item(
            Key={'OrderId': order_id},
            UpdateExpression="SET OrderStatus = :status",
            ExpressionAttributeValues={':status': 'COMPLETED'}
        )
        eventbridge.put_events(
            Entries=[
                {'Source': 'custom.order', 'DetailType': 'OrderCompleted', 'Detail': json.dumps({'order_id': order_id, 'status': 'COMPLETED'})}
            ]
        )