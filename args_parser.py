import argparse
import logging
import re
import sys
from constants import default_args
from attacker import Mode


def get_parser():
    parser = argparse.ArgumentParser(
        description="Slow HTTP Attacker, a tool providing three types of slow HTTP attack."
    )
    parser.add_argument("url", nargs="?", help='URL to perform stress test on. ("http[s]://<host>[:port][/path]")')
    parser.add_argument(
        "-m", "--mode", default=default_args['mode'],
        help='Mode of attack. The supported options are "HEADER", "POST" and "READ". ("header" by default)',
        type=str
    )
    parser.add_argument(
        "-s",
        "--sockets",
        default=default_args['sockets'],
        help="Number of sockets to use in the test (150 by default)",
        type=int,
    )
    parser.add_argument(
        "-d",
        "--duration",
        default=default_args['duration'],
        help="The duration of the attack (30 by default, and -1 means sustained attack)",
        type=int,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        help="Increases logging (False by default)",
    )
    parser.add_argument(
        "-ua",
        "--randuseragent",
        dest="randuseragent",
        action="store_true",
        help="Randomizes user-agents with each request (False by default)",
    )
    parser.add_argument(
        "--sleeptime",
        dest="sleeptime",
        default=default_args['sleeptime'],
        type=int,
        help="Time to sleep between beats used in HEADER and POST mode (15 by default)",
    )
    parser.add_argument(
        "-w", "--window",
        dest="window",
        default=default_args['window'],
        type=int,
        help="The window size used in READ mode (1 by default)",
    )
    parser.set_defaults(verbose=default_args['verbose'])
    parser.set_defaults(randuseragent=default_args['randuseragent'])
    return parser


def console_get_args_dict():
    """
    以控制台的方式运行，返回获取到的参数字典
    :return:
    """
    parser = get_parser()
    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)
    return vars(parser.parse_args())


def process_args_dict(d):
    """
    处理参数字典，包括参数合法性分析、verbose 设置、参数默认值填充和参数提取等
    :param d: 参数字典
    :return: 返回可以直接传入 Attacker __init__ 函数的参数
    """
    if d.get('url') is None:
        parser = get_parser()
        parser.print_help()
        sys.exit(1)

    for k, v in default_args.items():
        d.setdefault(k, v)
    d['mode'] = d['mode'].upper()
    # 在 API 调用时可能传入表示数字的字符串类型，例如字符串 "1024"
    d['sockets'] = int(d['sockets'])
    d['sleeptime'] = int(d['sleeptime'])
    d['duration'] = int(d['duration'])
    d['window'] = int(d['window'])

    if d['mode'] not in ['HEADER', 'POST', 'READ']:
        print('Unsupported mode. The supported modes are "HEADER", "POST" and "READ".')
        sys.exit(1)

    if d['verbose']:
        logging.basicConfig(
            format="[%(asctime)s] %(message)s",
            datefmt="%d-%m-%Y %H:%M:%S",
            level=logging.DEBUG,
        )
    else:
        logging.basicConfig(
            format="[%(asctime)s] %(message)s",
            datefmt="%d-%m-%Y %H:%M:%S",
            level=logging.INFO,
        )

    m = re.fullmatch(r'(?P<protocol>https?)://(?P<host>[^:/]*)(:(?P<port>\d*))?(?P<path>/.*)?', d['url'])
    if m is None:
        print('URL needs to be like "http[s]://<host>[:port][/path]"')
        sys.exit(1)
    https = True if m.group('protocol') == 'https' else False
    host = m.group('host')
    port = int(m.group('port')) if m.group('port') is not None else (443 if https else 80)
    path = m.group('path') if m.group('path') is not None else '/'
    return d['sockets'], Mode[d['mode']], host, port, path, d['duration'], d['sleeptime'], https, d['randuseragent'], d['window']
