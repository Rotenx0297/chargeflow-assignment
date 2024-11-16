import json
import boto3
import os

eventbridge = boto3.client('events')

EVENT_BUS_NAME = os.environ['EVENT_BUS_NAME']

def lambda_handler(event, context):
    body = json.loads(event['body'])
    event_detail = {
        'OrderId': body.get('orderId'),
        'CustomerName': body.get('customerName'),
        'Items': body.get('items'),
        'Timestamp': body.get('timestamp')
    }
    event = {
        'Entries': [
            {
                'Source': 'com.ordersystem.order',
                'DetailType': 'OrderCreated',       
                'Detail': json.dumps(event_detail), 
                'EventBusName': EVENT_BUS_NAME      
            }
        ]
    }

    try:
        response = eventbridge.put_events(**event)
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Order created successfully and event sent to EventBridge',
                'eventId': response['Entries'][0].get('EventId')
            })
        }

    except Exception as e:
        print(f"Error sending event to EventBridge: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Failed to process the order',
                'error': str(e)
            })
        }