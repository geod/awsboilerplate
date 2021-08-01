import json
import os
import unittest
import boto3
# import mock
# from moto import mock_s3
# from moto import mock_dynamodb2

# @mock_s3
# @mock_dynamodb2
# @mock.patch.dict(os.environ, {'DB_TABLE_NAME': DYNAMODB_TABLE_NAME})
class TestLambdaFunction(unittest.TestCase):

    # def setUp(self):
        # S3 setup
        # self.s3 = boto3.resource('s3', region_name=DEFAULT_REGION)
        # self.s3_bucket = self.s3.create_bucket(Bucket=S3_BUCKET_NAME)
        # self.s3_bucket.put_object(Key=S3_TEST_FILE_KEY,
        #                           Body=json.dumps(S3_TEST_FILE_CONTENT))
        #
        # # DynamoDB setup
        # self.dynamodb = boto3.client('dynamodb')
        # try:
        #     self.table = self.dynamodb.create_table(
        #         TableName=DYNAMODB_TABLE_NAME,
        #         KeySchema=[
        #             {'KeyType': 'HASH', 'AttributeName': 'product'}
        #         ],
        #         AttributeDefinitions=[
        #             {'AttributeName': 'product', 'AttributeType': 'S'}
        #         ],
        #         ProvisionedThroughput={
        #             'ReadCapacityUnits': 5,
        #             'WriteCapacityUnits': 5
        #         }
        #     )
        # except self.dynamodb.exceptions.ResourceInUseException:
        #     self.table = boto3.resource('dynamodb').Table(DYNAMODB_TABLE_NAME)


    def test_handler(self):
        event = {
            'Records': [
                {
                    's3': {
                        'bucket': {
                            'name': 'S3_BUCKET_NAME'
                        },
                        'object': {
                            'key': 'S3_TEST_FILE_KEY'
                        }
                    }
                }
            ]
        }

        result = (event, {})
        self.assertEqual(result, {'StatusCode': 200, 'Message': 'SUCCESS'})