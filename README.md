This Repo contains:
*  yaml template file for deploying all SAM resources in Cloudformation
*  src directory which contains all lambdas functions python code
*  github workflow file which is triggered on push to main branch and deploys the SAM stack to my private AWS Account (ID: 503161568134) using github managed runners

How to test:
*  Trigger a request via Apigw using curl command and receive an SNS email with the order status

Example:
*  When running to following command from terminal:
      curl -X POST -H "Content-Type: application/json" -d '{"orderId": "12345", "customerName": "Rotem Levy", "items": [{"itemId": "shirt", "quantity": 2},{"itemId": "pants", "quantity": 1}]}' https://sp2cadwlal.execute-api.us-east-1.amazonaws.com/Prod/order
    Output will be:
      {"message": "Order created successfully and event sent to EventBridge", "eventId": "77ed022c-a12f-890c-919a-d216c9c291c6"}
*  The DDB will contain the record:
        {
             "OrderId": {
              "S": "12345"
             },
             "CustomerName": {
              "S": "Rotem Levy"
             },
             "OrderStatus": {
              "S": "COMPLETED"
             }
        }
*  A message will be sent to the email Rotenx0297@gmail.com:
      
      Your order 12345 is now OrderCompleted.
      --
      If you wish to stop receiving notifications from this topic, please click or visit the link below to unsubscribe:
      https://sns.us-east-1.amazonaws.com/unsubscribe.html?SubscriptionArn=arn:aws:sns:us-east-1:503161568134:OrderNotificationTopic:c2867335-84e0-45df-9cb2-035c772cd992&Endpoint=Rotenx0297@gmail.com
      
      Please do not reply directly to this email. If you have any questions or comments regarding this email, please contact us at https://aws.amazon.com/support
