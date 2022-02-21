import string, random
from .models import Address


def link_generator(length: int):
    num = '0123456789'
    letter = string.ascii_letters
    raw = num + letter
    return ''.join(random.sample(raw, length))


def address_link(request):
    address = Address.objects.filter(user=request.user)
    if address.exists():
        address = address.filter(default=True)
        if address.exists:
            return True
    return False

