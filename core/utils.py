import string, random


def code_generator(length: int):
    letter = string.ascii_letters
    num = '0123456789`'
    raw = num + letter
    return ''.join(random.sample(raw, length))


def link_generator(link: str):
    bad_chars = [';', ':', '!', "*", '!', '@', '#', '$', '%', '^', '(', ')']
    link = link.replace(' ', '-')

    if '&' in link:
        link = link.replace('&', 'n')

    for i in bad_chars:
        if i in link:
            link = link.replace(i, '-')

    while True:
        if link[-1] == '-':
            link = link[:-1]
        else:
            break

    return link.lower()


def b_url(back):
    if back is not None:
        """ 1 is for post and 3 is for products """
        if back == '1':
            return True
        return False
