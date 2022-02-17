from django.shortcuts import render
from django.views.generic import *
from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

Order = apps.get_model('core', 'Order')
OrderItem = apps.get_model('core', 'OrderItem')


class OrderSummary(ListView, LoginRequiredMixin):
    model = Order
    template_name = None
    context_object_name = 'items'

    def get_queryset(self):
        return Order.objects.get(user=self.request.user, ordered=False)


