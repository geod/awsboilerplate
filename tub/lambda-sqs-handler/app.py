import boto3
import os

queue_name = os.environ['SQS_NAME']
sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName=queue_name)


def handler(event, context):
    #PLACEHOLDER - customize the validation logic

    response = queue.send_message(MessageBody='world')
    print(response.get('MessageId'))
    print(response.get('MD5OfMessageBody'))
    return ''
