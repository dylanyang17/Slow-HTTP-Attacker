import logging
import json
from attacker import Attacker
from args_parser import process_args_dict


def tencent_run_test(event, context):
    logging.info('Tencent Serverless.')
    logging.info(context)
    args = process_args_dict(event)
    attacker = Attacker(*args)
    attacker.attack()


def tencent_run_api(event, context):
    logging.info('Tencent Serverless.')
    logging.info(context)
    args = process_args_dict(event['queryString'])
    attacker = Attacker(*args)
    attacker.attack()


def aliyun_run_test(event, context):
    logging.info('Aliyun Serverless.')
    logging.info(context)
    args = process_args_dict(json.loads(event))
    attacker = Attacker(*args)
    attacker.attack()


def huawei_run_test(event, context):
    logging.info('Huawei Serverless.')
    logging.info(context)
    args = process_args_dict(event)
    attacker = Attacker(*args)
    attacker.attack()
