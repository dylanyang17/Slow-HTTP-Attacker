import argparse
import logging
import re
import sys


def get_args():
    parser = argparse.ArgumentParser(
        description="Slow HTTP Attacker, a tool providing three types of slow HTTP attack."
    )
    parser.add_argument("url", nargs="?", help='URL to perform stress test on. ("http[s]://<host>[:port][/path]")')
    parser.add_argument(
        "-m", "--mode", default='HEADER',
        help='Mode of attack. The supported options are "HEADER", "POST" and "READ". ("header" by default)',
        type=str
    )
    parser.add_argument(
        "-s",
        "--sockets",
        default=150,
        help="Number of sockets to use in the test (150 by default)",
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
        "--randuseragents",
        dest="randuseragent",
        action="store_true",
        help="Randomizes user-agents with each request (False by default)",
    )
    parser.add_argument(
        "--sleeptime",
        dest="sleeptime",
        default=15,
        type=int,
        help="Time to sleep between beats used in HEADER and POST mode (15 by default)",
    )
    parser.add_argument(
        "-w", "--window",
        dest="window",
        default=1,
        type=int,
        help="The window size used in READ mode (1 by default)",
    )
    parser.set_defaults(verbose=False)
    parser.set_defaults(randuseragent=False)

    args = parser.parse_args()

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)

    args.mode = args.mode.upper()

    if args.mode not in ['HEADER', 'POST', 'READ']:
        print('Unsupported mode. The supported modes are "HEADER", "POST" and "READ".')
        sys.exit(1)

    if args.verbose:
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

    m = re.fullmatch(r'(?P<protocol>https?)://(?P<host>[^:/]*)(:(?P<port>\d*))?(?P<path>/.*)?', args.url)
    if m is None:
        print('URL needs to be like "http[s]://<host>[:port][/path]"')
        sys.exit(1)
    https = True if m.group('protocol') == 'https' else False
    host = m.group('host')
    port = int(m.group('port')) if m.group('port') is not None else (443 if https else 80)
    path = m.group('path') if m.group('path') is not None else '/'
    return args, https, host, port, path
