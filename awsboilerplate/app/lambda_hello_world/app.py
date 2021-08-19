import json

def handler(event, context):
    to = event["queryStringParameters"]['to']
    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True
        },
        "body": json.dumps({
            "message": "Hello " + to
        })
    }
    return response
