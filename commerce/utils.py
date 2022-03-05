import random, string


def link_generator(length) -> str:
    letters = string.ascii_letters
    num = '0123456789'
    raw = letters + num
    return ''.join(random.sample(raw, length))
