import logging


def send_utf8(sock, s):
    logging.debug('send: ' + s)
    sock.send(s.encode("utf-8"))


def send_line(sock, line=""):
    line = f"{line}\r\n"
    send_utf8(sock, line)


def send_header(sock, name, value):
    send_line(sock, f"{name}: {value}")
