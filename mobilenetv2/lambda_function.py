import json
import boto3
import numpy as np
from PIL import Image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.models import load_model
import time

bucket_name = 'imagenet-sample'
bucket_ensemble = 'lambda-ensemble'
model_name = 'mobilenet_v2'
model_path = '/var/task/lambda-ensemble-sequence/mobilenet_v2/model/' + model_name
model = load_model(model_path, compile=True)

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')

table_name = 'lambda-ensemble1'
region_name = 'us-west-2'
dynamodb = boto3.resource('dynamodb', region_name=region_name)
table = dynamodb.Table(table_name)


def upload_s3(case_num, acc):
    item_dict = dict([(str(i), str(acc[i])) for i in range(len(acc))])
    s3_client.put_object(
        Body=json.dumps(item_dict),
        Bucket=bucket_ensemble,
        Key=model_name + '_' + case_num + '.txt'
    )
    return True


def upload_dynamodb(case_num, acc):
    item_dict = dict([(str(i), str(acc[i])) for i in range(len(acc))])
    item_dict['model_name'] = model_name
    item_dict['case_num'] = case_num

    with table.batch_writer() as batch:
        batch.put_item(Item=item_dict)
    return True


def read_image_from_s3(filename):
    bucket = s3.Bucket(bucket_name)
    object = bucket.Object(filename)
    response = object.get()
    file_stream = response['Body']
    img = Image.open(file_stream)
    img.convert('RGB')
    return img


def filenames_to_input(file_list):
    imgs = []
    for file in file_list:
        img = read_image_from_s3(file)
        img = img.resize((224, 224), Image.ANTIALIAS)
        img = np.array(img)
        # if image is grayscale, convert to 3 channels
        if len(img.shape) != 3:
            img = np.repeat(img[..., np.newaxis], 3, -1)
        # batchsize, 224, 224, 3
        img = img.reshape((1, img.shape[0], img.shape[1], img.shape[2]))
        img = preprocess_input(img)
        imgs.append(img)

    batch_imgs = np.vstack(imgs)
    return batch_imgs


def inference_model(batch_imgs):
    pred_start = time.time()
    result = model.predict(batch_imgs)
    pred_time = time.time() - pred_start

    result = np.round(result.astype(np.float64), 8)
    result = result.tolist()

    return result, pred_time


def lambda_handler(event, context):
    file_list = event['file_list']
    batch_size = event['batch_size']
    case_num = event['case_num']
    batch_imgs = filenames_to_input(file_list)

    total_start = time.time()
    result, pred_time = inference_model(batch_imgs)
    upload_s3(case_num, result)
    total_time = time.time() - total_start

    return {
        'file_list': file_list,
        'model_name': model_name,
        'case_num': case_num,
        'batch_size': batch_size,
        'total_time': total_time,
        'pred_time': pred_time,
    }
