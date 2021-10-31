import json
import boto3
import time

BUCKET_NAME = 'imagenet-sample'

s3 = boto3.resource('s3')


def lambda_handler(event, context):
    start_time = str(time.time())
    batch_size = event['batch_size']
    bucket = s3.Bucket(BUCKET_NAME)
    filenames = [file.key for file in bucket.objects.all() if len(file.key.split('/')[1]) > 1]
    filenames = filenames[batch_size[0]:batch_size[1]]

    return {
        'file_list': filenames,
        'batch_size': batch_size[1] - batch_size[0],
        'case_num': start_time
    }
