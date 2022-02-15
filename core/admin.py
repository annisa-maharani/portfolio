from django.contrib.admin import site
from .models import *

site.register(Item)
site.register(OrderItem)
site.register(Order)
site.register(Coupon)