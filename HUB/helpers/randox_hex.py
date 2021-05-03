import random
import string


def random_hex(num):
    return ''.join(random.choice(string.hexdigits) for _ in range(num))