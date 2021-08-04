import boto3
import os
import json
queue_name = os.environ['SQS_NAME']
sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName=queue_name)


def handler(event, context):
    #PLACEHOLDER - customize the validation logic

    response = queue.send_message(MessageBody='world')
    print(response.get('MessageId'))
    print(response.get('MD5OfMessageBody'))

    response = {
        "statusCode": 200,
        "headers": {},
        "body": json.dumps({
            "message": "This is the message in a JSON object."
        })
    }
    return response
