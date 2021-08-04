import boto3
import os
import uuid
from urllib.parse import unquote_plus

source_bucket_name = os.environ['RAW_BUCKET']
target_bucket_name = os.environ['PROCESSED_BUCKET']
s3_client = boto3.client('s3')

def handler(event, context):
    '''
    Handler - will be called on *each* file update / no batching
    :param event:
    :param context:
    :return:
    '''
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        tmpkey = key.replace('/', '')
        tmp_download_path = '/tmp/{}{}'.format(uuid.uuid4(), tmpkey)
        tmp_upload_path = '/tmp/resized-{}'.format(tmpkey)
        s3_client.download_file(bucket, key, tmp_download_path)

        print(f'download:{tmp_download_path} upload:{tmp_upload_path}')
        # process file (tmp_download_path, tmp_upload_path)

        #s3_client.upload_file(tmp_upload_path, '{}-resized'.format(bucket), key)
