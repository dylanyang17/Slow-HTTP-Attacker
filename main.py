from args_parser import process_args_dict, get_args_dict
from attacker import Attacker, Mode


if __name__ == "__main__":
    # print(get_args())
    args = process_args_dict(get_args_dict())
    attacker = Attacker(*args)
    attacker.attack()
