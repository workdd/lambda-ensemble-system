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
        actual_labels = [int(label.split('/')[1].split('_')[0][1:]) for label in data[0]['file_list']]
    else:
        models = ['mobilenet_v2', 'efficientnetb0', 'nasnetmobile']
        for m in models:
            try:
                filename = m + '_' + data['case_num'] + '.txt'
                object = bucket.Object(filename)
                res = object.get()
                res = json.load(res['Body'])
                res = list(res.values())
                res = [ast.literal_eval(val) for val in res]
                response.append(res)
            except:
                pass
        actual_labels = [int(label.split('/')[1].split('_')[0][1:]) for label in data['file_list']]
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
    with open('imagenet_class_index.json') as f:
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
        pred_labels += [int(img_class[1:]) for img_class, label, acc in single_result]
    print(np.array(pred_labels))
    print(np.array(actual_labels))
    acc = np.sum(np.array(actual_labels) == np.array(pred_labels)) / len(actual_labels)
    print(acc)
    return {
        'result': results,
        'get_time': get_time,
        'total_time': time.time() - get_start,
        'fin_time': time.time(),
        'accuracy': acc
    }


event = [
    {
        "file_list": [
            "imagenet-sample-images/n01443537_goldfish.JPEG",
            "imagenet-sample-images/n01484850_great_white_shark.JPEG",
            "imagenet-sample-images/n01491361_tiger_shark.JPEG",
            "imagenet-sample-images/n01494475_hammerhead.JPEG",
            "imagenet-sample-images/n01496331_electric_ray.JPEG",
            "imagenet-sample-images/n01498041_stingray.JPEG",
            "imagenet-sample-images/n01514668_cock.JPEG",
            "imagenet-sample-images/n01514859_hen.JPEG",
            "imagenet-sample-images/n01518878_ostrich.JPEG",
            "imagenet-sample-images/n01530575_brambling.JPEG",
            "imagenet-sample-images/n01531178_goldfinch.JPEG",
            "imagenet-sample-images/n01532829_house_finch.JPEG",
            "imagenet-sample-images/n01534433_junco.JPEG",
            "imagenet-sample-images/n01537544_indigo_bunting.JPEG",
            "imagenet-sample-images/n01558993_robin.JPEG",
            "imagenet-sample-images/n01560419_bulbul.JPEG",
            "imagenet-sample-images/n01580077_jay.JPEG",
            "imagenet-sample-images/n01582220_magpie.JPEG",
            "imagenet-sample-images/n01592084_chickadee.JPEG",
            "imagenet-sample-images/n01601694_water_ouzel.JPEG",
            "imagenet-sample-images/n01608432_kite.JPEG",
            "imagenet-sample-images/n01614925_bald_eagle.JPEG",
            "imagenet-sample-images/n01616318_vulture.JPEG",
            "imagenet-sample-images/n01622779_great_grey_owl.JPEG",
            "imagenet-sample-images/n01629819_European_fire_salamander.JPEG",
            "imagenet-sample-images/n01630670_common_newt.JPEG",
            "imagenet-sample-images/n01631663_eft.JPEG",
            "imagenet-sample-images/n01632458_spotted_salamander.JPEG",
            "imagenet-sample-images/n01632777_axolotl.JPEG",
            "imagenet-sample-images/n01641577_bullfrog.JPEG",
            "imagenet-sample-images/n01644373_tree_frog.JPEG",
            "imagenet-sample-images/n01644900_tailed_frog.JPEG",
            "imagenet-sample-images/n01664065_loggerhead.JPEG",
            "imagenet-sample-images/n01665541_leatherback_turtle.JPEG",
            "imagenet-sample-images/n01667114_mud_turtle.JPEG",
            "imagenet-sample-images/n01667778_terrapin.JPEG",
            "imagenet-sample-images/n01669191_box_turtle.JPEG",
            "imagenet-sample-images/n01675722_banded_gecko.JPEG",
            "imagenet-sample-images/n01677366_common_iguana.JPEG",
            "imagenet-sample-images/n01682714_American_chameleon.JPEG",
            "imagenet-sample-images/n01685808_whiptail.JPEG",
            "imagenet-sample-images/n01687978_agama.JPEG",
            "imagenet-sample-images/n01688243_frilled_lizard.JPEG",
            "imagenet-sample-images/n01689811_alligator_lizard.JPEG",
            "imagenet-sample-images/n01692333_Gila_monster.JPEG",
            "imagenet-sample-images/n01693334_green_lizard.JPEG",
            "imagenet-sample-images/n01694178_African_chameleon.JPEG",
            "imagenet-sample-images/n01695060_Komodo_dragon.JPEG",
            "imagenet-sample-images/n01697457_African_crocodile.JPEG",
            "imagenet-sample-images/n01698640_American_alligator.JPEG",
            "imagenet-sample-images/n01704323_triceratops.JPEG",
            "imagenet-sample-images/n01728572_thunder_snake.JPEG",
            "imagenet-sample-images/n01728920_ringneck_snake.JPEG",
            "imagenet-sample-images/n01729322_hognose_snake.JPEG",
            "imagenet-sample-images/n01729977_green_snake.JPEG",
            "imagenet-sample-images/n01734418_king_snake.JPEG",
            "imagenet-sample-images/n01735189_garter_snake.JPEG",
            "imagenet-sample-images/n01737021_water_snake.JPEG",
            "imagenet-sample-images/n01739381_vine_snake.JPEG",
            "imagenet-sample-images/n01740131_night_snake.JPEG",
            "imagenet-sample-images/n01742172_boa_constrictor.JPEG",
            "imagenet-sample-images/n01744401_rock_python.JPEG",
            "imagenet-sample-images/n01748264_Indian_cobra.JPEG",
            "imagenet-sample-images/n01749939_green_mamba.JPEG"
        ],
        "model_name": "efficientnetb0",
        "case_num": "1635724784.604815",
        "batch_size": 64,
        "total_time": 4.249855995178223,
        "pred_time": 4.07789945602417
    },
    {
        "file_list": [
            "imagenet-sample-images/n01443537_goldfish.JPEG",
            "imagenet-sample-images/n01484850_great_white_shark.JPEG",
            "imagenet-sample-images/n01491361_tiger_shark.JPEG",
            "imagenet-sample-images/n01494475_hammerhead.JPEG",
            "imagenet-sample-images/n01496331_electric_ray.JPEG",
            "imagenet-sample-images/n01498041_stingray.JPEG",
            "imagenet-sample-images/n01514668_cock.JPEG",
            "imagenet-sample-images/n01514859_hen.JPEG",
            "imagenet-sample-images/n01518878_ostrich.JPEG",
            "imagenet-sample-images/n01530575_brambling.JPEG",
            "imagenet-sample-images/n01531178_goldfinch.JPEG",
            "imagenet-sample-images/n01532829_house_finch.JPEG",
            "imagenet-sample-images/n01534433_junco.JPEG",
            "imagenet-sample-images/n01537544_indigo_bunting.JPEG",
            "imagenet-sample-images/n01558993_robin.JPEG",
            "imagenet-sample-images/n01560419_bulbul.JPEG",
            "imagenet-sample-images/n01580077_jay.JPEG",
            "imagenet-sample-images/n01582220_magpie.JPEG",
            "imagenet-sample-images/n01592084_chickadee.JPEG",
            "imagenet-sample-images/n01601694_water_ouzel.JPEG",
            "imagenet-sample-images/n01608432_kite.JPEG",
            "imagenet-sample-images/n01614925_bald_eagle.JPEG",
            "imagenet-sample-images/n01616318_vulture.JPEG",
            "imagenet-sample-images/n01622779_great_grey_owl.JPEG",
            "imagenet-sample-images/n01629819_European_fire_salamander.JPEG",
            "imagenet-sample-images/n01630670_common_newt.JPEG",
            "imagenet-sample-images/n01631663_eft.JPEG",
            "imagenet-sample-images/n01632458_spotted_salamander.JPEG",
            "imagenet-sample-images/n01632777_axolotl.JPEG",
            "imagenet-sample-images/n01641577_bullfrog.JPEG",
            "imagenet-sample-images/n01644373_tree_frog.JPEG",
            "imagenet-sample-images/n01644900_tailed_frog.JPEG",
            "imagenet-sample-images/n01664065_loggerhead.JPEG",
            "imagenet-sample-images/n01665541_leatherback_turtle.JPEG",
            "imagenet-sample-images/n01667114_mud_turtle.JPEG",
            "imagenet-sample-images/n01667778_terrapin.JPEG",
            "imagenet-sample-images/n01669191_box_turtle.JPEG",
            "imagenet-sample-images/n01675722_banded_gecko.JPEG",
            "imagenet-sample-images/n01677366_common_iguana.JPEG",
            "imagenet-sample-images/n01682714_American_chameleon.JPEG",
            "imagenet-sample-images/n01685808_whiptail.JPEG",
            "imagenet-sample-images/n01687978_agama.JPEG",
            "imagenet-sample-images/n01688243_frilled_lizard.JPEG",
            "imagenet-sample-images/n01689811_alligator_lizard.JPEG",
            "imagenet-sample-images/n01692333_Gila_monster.JPEG",
            "imagenet-sample-images/n01693334_green_lizard.JPEG",
            "imagenet-sample-images/n01694178_African_chameleon.JPEG",
            "imagenet-sample-images/n01695060_Komodo_dragon.JPEG",
            "imagenet-sample-images/n01697457_African_crocodile.JPEG",
            "imagenet-sample-images/n01698640_American_alligator.JPEG",
            "imagenet-sample-images/n01704323_triceratops.JPEG",
            "imagenet-sample-images/n01728572_thunder_snake.JPEG",
            "imagenet-sample-images/n01728920_ringneck_snake.JPEG",
            "imagenet-sample-images/n01729322_hognose_snake.JPEG",
            "imagenet-sample-images/n01729977_green_snake.JPEG",
            "imagenet-sample-images/n01734418_king_snake.JPEG",
            "imagenet-sample-images/n01735189_garter_snake.JPEG",
            "imagenet-sample-images/n01737021_water_snake.JPEG",
            "imagenet-sample-images/n01739381_vine_snake.JPEG",
            "imagenet-sample-images/n01740131_night_snake.JPEG",
            "imagenet-sample-images/n01742172_boa_constrictor.JPEG",
            "imagenet-sample-images/n01744401_rock_python.JPEG",
            "imagenet-sample-images/n01748264_Indian_cobra.JPEG",
            "imagenet-sample-images/n01749939_green_mamba.JPEG"
        ],
        "model_name": "nasnetmobile",
        "case_num": "1635724784.604815",
        "batch_size": 64,
        "total_time": 6.82188081741333,
        "pred_time": 6.667876720428467
    },
    {
        "file_list": [
            "imagenet-sample-images/n01443537_goldfish.JPEG",
            "imagenet-sample-images/n01484850_great_white_shark.JPEG",
            "imagenet-sample-images/n01491361_tiger_shark.JPEG",
            "imagenet-sample-images/n01494475_hammerhead.JPEG",
            "imagenet-sample-images/n01496331_electric_ray.JPEG",
            "imagenet-sample-images/n01498041_stingray.JPEG",
            "imagenet-sample-images/n01514668_cock.JPEG",
            "imagenet-sample-images/n01514859_hen.JPEG",
            "imagenet-sample-images/n01518878_ostrich.JPEG",
            "imagenet-sample-images/n01530575_brambling.JPEG",
            "imagenet-sample-images/n01531178_goldfinch.JPEG",
            "imagenet-sample-images/n01532829_house_finch.JPEG",
            "imagenet-sample-images/n01534433_junco.JPEG",
            "imagenet-sample-images/n01537544_indigo_bunting.JPEG",
            "imagenet-sample-images/n01558993_robin.JPEG",
            "imagenet-sample-images/n01560419_bulbul.JPEG",
            "imagenet-sample-images/n01580077_jay.JPEG",
            "imagenet-sample-images/n01582220_magpie.JPEG",
            "imagenet-sample-images/n01592084_chickadee.JPEG",
            "imagenet-sample-images/n01601694_water_ouzel.JPEG",
            "imagenet-sample-images/n01608432_kite.JPEG",
            "imagenet-sample-images/n01614925_bald_eagle.JPEG",
            "imagenet-sample-images/n01616318_vulture.JPEG",
            "imagenet-sample-images/n01622779_great_grey_owl.JPEG",
            "imagenet-sample-images/n01629819_European_fire_salamander.JPEG",
            "imagenet-sample-images/n01630670_common_newt.JPEG",
            "imagenet-sample-images/n01631663_eft.JPEG",
            "imagenet-sample-images/n01632458_spotted_salamander.JPEG",
            "imagenet-sample-images/n01632777_axolotl.JPEG",
            "imagenet-sample-images/n01641577_bullfrog.JPEG",
            "imagenet-sample-images/n01644373_tree_frog.JPEG",
            "imagenet-sample-images/n01644900_tailed_frog.JPEG",
            "imagenet-sample-images/n01664065_loggerhead.JPEG",
            "imagenet-sample-images/n01665541_leatherback_turtle.JPEG",
            "imagenet-sample-images/n01667114_mud_turtle.JPEG",
            "imagenet-sample-images/n01667778_terrapin.JPEG",
            "imagenet-sample-images/n01669191_box_turtle.JPEG",
            "imagenet-sample-images/n01675722_banded_gecko.JPEG",
            "imagenet-sample-images/n01677366_common_iguana.JPEG",
            "imagenet-sample-images/n01682714_American_chameleon.JPEG",
            "imagenet-sample-images/n01685808_whiptail.JPEG",
            "imagenet-sample-images/n01687978_agama.JPEG",
            "imagenet-sample-images/n01688243_frilled_lizard.JPEG",
            "imagenet-sample-images/n01689811_alligator_lizard.JPEG",
            "imagenet-sample-images/n01692333_Gila_monster.JPEG",
            "imagenet-sample-images/n01693334_green_lizard.JPEG",
            "imagenet-sample-images/n01694178_African_chameleon.JPEG",
            "imagenet-sample-images/n01695060_Komodo_dragon.JPEG",
            "imagenet-sample-images/n01697457_African_crocodile.JPEG",
            "imagenet-sample-images/n01698640_American_alligator.JPEG",
            "imagenet-sample-images/n01704323_triceratops.JPEG",
            "imagenet-sample-images/n01728572_thunder_snake.JPEG",
            "imagenet-sample-images/n01728920_ringneck_snake.JPEG",
            "imagenet-sample-images/n01729322_hognose_snake.JPEG",
            "imagenet-sample-images/n01729977_green_snake.JPEG",
            "imagenet-sample-images/n01734418_king_snake.JPEG",
            "imagenet-sample-images/n01735189_garter_snake.JPEG",
            "imagenet-sample-images/n01737021_water_snake.JPEG",
            "imagenet-sample-images/n01739381_vine_snake.JPEG",
            "imagenet-sample-images/n01740131_night_snake.JPEG",
            "imagenet-sample-images/n01742172_boa_constrictor.JPEG",
            "imagenet-sample-images/n01744401_rock_python.JPEG",
            "imagenet-sample-images/n01748264_Indian_cobra.JPEG",
            "imagenet-sample-images/n01749939_green_mamba.JPEG"
        ],
        "model_name": "mobilenet_v2",
        "case_num": "1635724784.604815",
        "batch_size": 64,
        "total_time": 2.639417886734009,
        "pred_time": 2.472555160522461
    }
]

context = 0
lambda_handler(event, context)
