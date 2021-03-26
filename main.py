from args_parser import get_args
from attacker import Attacker, Mode


if __name__ == "__main__":
    # print(get_args())
    args, https, host, port, path = get_args()
    attacker = Attacker(args.sockets, Mode[args.mode.upper()], host, port, path, args.sleeptime, https, args.randuseragent, args.window)
    attacker.attack()
