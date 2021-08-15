import json

def handler(event, context):
    to = event["queryStringParameters"]['say']
    response = {
        "statusCode": 200,
        "headers": {},
        "body": json.dumps({
            "message": "Hello " + to
        })
    }
    return response
