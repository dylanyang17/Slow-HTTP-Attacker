import argparse
import logging
import socket
import sys


def get_args():
    parser = argparse.ArgumentParser(
        description="Slow HTTP Attacker, a tool providing three types of slow HTTP attack."
    )
    parser.add_argument("host", nargs="?", help="Host to perform stress test on")
    parser.add_argument(
        "-m", "--mode", default='header', help='Mode of attack. The supported options are "header", "post" and "read"',
        type=str
    )
    parser.add_argument(
        "-p", "--port", default=80, help="Port of webserver, usually 80", type=int
    )
    parser.add_argument(
        "-s",
        "--sockets",
        default=150,
        help="Number of sockets to use in the test",
        type=int,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        help="Increases logging",
    )
    parser.add_argument(
        "-ua",
        "--randuseragents",
        dest="randuseragent",
        action="store_true",
        help="Randomizes user-agents with each request",
    )
    # parser.add_argument(
    #     "-x",
    #     "--useproxy",
    #     dest="useproxy",
    #     action="store_true",
    #     help="Use a SOCKS5 proxy for connecting",
    # )
    # parser.add_argument(
    #     "--proxy-host", default="127.0.0.1", help="SOCKS5 proxy host"
    # )
    # parser.add_argument(
    #     "--proxy-port", default="8080", help="SOCKS5 proxy port", type=int
    # )
    parser.add_argument(
        "--https",
        dest="https",
        action="store_true",
        help="Use HTTPS for the requests",
    )
    parser.add_argument(
        "--sleeptime",
        dest="sleeptime",
        default=15,
        type=int,
        help="Time to sleep after sending a beat",
    )
    parser.set_defaults(verbose=False)
    parser.set_defaults(randuseragent=False)
    # parser.set_defaults(useproxy=False)
    parser.set_defaults(https=False)

    args = parser.parse_args()

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)

    args.mode = args.mode.lower()

    if args.mode not in ['header', 'post', 'read']:
        print('Unsupported mode. The supported modes are "header", "post" and "read".')
        sys.exit(1)

    if not args.host:
        print("Host required!")
        parser.print_help()
        sys.exit(1)

    # if args.useproxy:
    #     # Tries to import to external "socks" library
    #     # and monkey patches socket.socket to connect over
    #     # the proxy by default
    #     try:
    #         import socks
    #
    #         socks.setdefaultproxy(
    #             socks.PROXY_TYPE_SOCKS5, args.proxy_host, args.proxy_port
    #         )
    #         socket.socket = socks.socksocket
    #         logging.info("Using SOCKS5 proxy for connecting...")
    #     except ImportError:
    #         logging.error("Socks Proxy Library Not Available!")

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

    return args
