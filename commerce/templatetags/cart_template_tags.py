from django import template
from django.apps import apps

Order = apps.get_model('core', 'Order')
count: int
register = template.Library()

@register.filter
def cart_item_counter(user):
    global count
    if user.is_authenticated:
        count = 0
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            qs = qs.first()
            for quantity in qs.item.all():
                count += quantity.quantity
        return count
    return 0
