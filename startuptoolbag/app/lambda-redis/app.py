import redis
import json

import uuid
import os


#elasticache settings
cache_address = os.environ['CACHE_ADDRESS']
cache_port = os.environ['CACHE_PORT ']
client = redis.Redis.from_url(f'redis://{cache_address}:{cache_port}', socket_timeout=3.0)


def handler(event, context):
    """
    This function puts into memcache and get from it.
    Memcache is hosted using elasticache
    """

    #Create a random UUID... this will be the sample element we add to the cache.
    uuid_inserted = uuid.uuid4().hex
    #Put the UUID to the cache.
    client.set('uuid', uuid_inserted)
    #Get item (UUID) from the cache.
    uuid_obtained = client.get('uuid')
    if uuid_obtained.decode("utf-8") == uuid_inserted:
        # this print should go to the CloudWatch Logs and Lambda console.
        print ("Success: Fetched value %s from memcache:" %(uuid_inserted))
    else:
        raise Exception("Value is not the same as we put :(. Expected %s got %s" %(uuid_inserted, uuid_obtained))

    return {
        'statusCode': 200,
        'body': json.dumps("Fetched value from memcache: " + uuid_obtained.decode("utf-8"))
    }

