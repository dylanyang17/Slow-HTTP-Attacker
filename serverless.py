from attacker import Attacker, Mode
import logging


def tencent_run(event, context):
    logging.info('Tencent Serverless.')
    print(type(event))
    print(event)
