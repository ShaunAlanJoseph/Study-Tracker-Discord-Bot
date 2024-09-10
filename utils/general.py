from time import time


def get_time() -> int:
    return int(1000 * time())