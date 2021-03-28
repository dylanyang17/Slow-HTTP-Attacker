from args_parser import get_args
from attacker import Attacker, Mode


def run(sockets, mode, host, port, path, sleeptime, https, randuseragent, window):
    """
    便于云函数调用，参数同 Attacker 的 __init__ 函数
    :param sockets: int，使用的套接字数目，也即线程数
    :param mode: Mode，攻击模式
    :param host: str，主机名
    :param port: int，端口号
    :param path: str，攻击路径
    :param sleeptime: int，两次 beats 之间的间隔时间，仅 HEADER 和 POST 模式有效
    :param https: boolean，是否使用 HTTPS
    :param randuseragent: boolean，是否使用随机的 User-Agent
    :param window: int，TCP 窗口大小，仅 READ 模式有效
    """
    attacker = Attacker(sockets, mode, host, port, path, sleeptime, https, randuseragent, window)
    attacker.attack()


if __name__ == "__main__":
    # print(get_args())
    args, https, host, port, path = get_args()
    run(args.sockets, Mode[args.mode.upper()], host, port, path, args.sleeptime, https, args.randuseragent, args.window)
