from __future__ import print_function
import json
import os
import uuid
import boto3
import decimal
import sympy


# Converts DynamoDB items to JSON
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


# Writes to this dynamodb
dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ['TABLE_NAME']

def handler(event, context):
    #TODO - process the message and perform the business logic

    # Write to table
    table = dynamodb.Table(TABLE_NAME)
    response = table.put_item(
        Item={
            'job_id': str(uuid.uuid4())
        }
    )
    print("PutItem succeeded:")
    print(json.dumps(response, indent=4, cls=DecimalEncoder))
    return ''
