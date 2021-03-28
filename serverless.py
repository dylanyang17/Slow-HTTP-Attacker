from attacker import Attacker
from args_parser import process_args_dict
import logging


def tencent_run(event, context):
    logging.info('Tencent Serverless.')
    logging.info(context)
    args = process_args_dict(event)
    attacker = Attacker(*args)
    attacker.attack()
