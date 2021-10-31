import json
import boto3
import numpy as np
import time
import ast

table_name = 'lambda-ensemble1'
bucket_ensemble = 'lambda-ensemble'
s3 = boto3.resource('s3')
region_name = 'us-west-2'
dynamodb = boto3.resource('dynamodb', region_name=region_name)
table = dynamodb.Table(table_name)


def get_s3(data):
    bucket = s3.Bucket(bucket_ensemble)
    response = []
    actual_labels = []
    if (isinstance(data, list)):
        for d in data:
            filename = d['model_name'] + '_' + d['case_num'] + '.txt'
            object = bucket.Object(filename)
            res = object.get()
            res = json.load(res['Body'])
            res = list(res.values())
            res = [ast.literal_eval(val) for val in res]
            response.append(res)
        actual_labels = [label.split('/')[1].split('_')[0] for label in data[0]['file_list']]
    else:
        models = ['mobilenet_v2', 'efficientnetb0', 'nasnetmobile']
        for m in models:
            filename = m + '_' + data['case_num'] + '.txt'
            object = bucket.Object(filename)
            res = object.get()
            res = json.load(res['Body'])
            res = list(res.values())
            res = [ast.literal_eval(val) for val in res]
            response.append(res)
        actual_labels = [label.split('/')[1].split('_')[0] for label in data['file_list']]
    response = np.array(response)
    response = response.astype(np.float)
    response = response.mean(axis=0)
    return response, actual_labels


def get_dynamodb(data):
    response = []
    for d in data:
        res = table.get_item(Key={"model_name": d['model_name'], "case_num": d['case_num']})
        res = res['Item']
        res.pop('model_name')
        res.pop('case_num')
        res = list(res.values())
        res = [ast.literal_eval(val) for val in res]
        response.append(res)
    response = np.array(response)
    response = response.astype(np.float)
    response = response.mean(axis=0)
    return response


def decode_predictions(preds, top=1):
    # get imagenet_class_index.json from container directory
    with open('/var/task/lambda-ensemble-sequence/ensemble/imagenet_class_index.json') as f:
        CLASS_INDEX = json.load(f)
    results = []
    for pred in preds:
        top_indices = pred.argsort()[-top:][::-1]
        result = [tuple(CLASS_INDEX[str(i)]) + (pred[i],) for i in top_indices]
        result.sort(key=lambda x: x[2], reverse=True)
        results.append(result)
    return results


def lambda_handler(event, context):
    results = []
    get_start = time.time()
    result, actual_labels = get_s3(event)
    get_time = time.time() - get_start
    result = decode_predictions(result)
    pred_labels = []
    for single_result in result:
        single_result = [(img_class, label, round(acc * 100, 4)) for img_class, label, acc in single_result]
        results += single_result
        pred_labels = [img_class for img_class, label, acc in single_result]

    acc = np.sum(np.array(actual_labels) == np.array(pred_labels)) / len(actual_labels)

    return {
        'result': results,
        'get_time': get_time,
        'total_time': time.time() - get_start,
        'fin_time': time.time(),
        'accuracy': acc
    }
