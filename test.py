import socket
import random
import ssl
import threading

from socket_utils import send_line, send_utf8, send_header
import logging

logging.basicConfig(
            format="[%(asctime)s] %(message)s",
            datefmt="%d-%m-%Y %H:%M:%S",
            level=logging.DEBUG,
        )


def main():
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # host = '120.53.3.109'
        # port = 8888
        host = 'yangyrremote.xyz'
        port = 80
        # s = ssl.wrap_socket(s)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1000)
        s.settimeout(4)
        s.connect((host, port))
        send_line(s, f"GET / HTTP/1.1")
        send_header(s, "Host", host)
        send_header(s, "User-Agent", "User-Agent: Opera/9.80 (Macintosh; Intel Mac OS X 10.7.0; U; Edition MacAppStore; en) Mozilla/5.0 (Macintosh; Intel Mac OS X) AppleWebKit/534.34 (KHTML,like Gecko) PhantomJS/1.9.0 (development) Safari/534.34")
        send_header(s, "Accept-language", "en-US,en,q=0.5")
        send_line(s)
        print(s.recv(1000))
        try:
            print(s.recv(1000))
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
    thread_pool = []
    thread_number = 5
    for i in range(0, thread_number):
        thread_pool.append(threading.Thread(target=main))
        thread_pool[i].start()
    for i in range(0, thread_number):
        thread_pool[i].join()
