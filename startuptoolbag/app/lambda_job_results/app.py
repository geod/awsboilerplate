from __future__ import print_function

import json
import decimal
import os
import boto3
from botocore.exceptions import ClientError


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ['TABLE_NAME']


def handler(event, context):
    table = dynamodb.Table(TABLE_NAME)
    # Scan items in table
    try:
        response = table.scan()
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        # print item of the table - see CloudWatch logs
        for i in response['Items']:
            print(json.dumps(i, cls=DecimalEncoder))

    response = {
        "statusCode": 200,
        "headers": {},
        "body": json.dumps({
            "message": "This is the message in a JSON object."
        })
    }
    return response