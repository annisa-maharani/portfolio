from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import *
from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse

Order = apps.get_model('core', 'Order')
OrderItem = apps.get_model('core', 'OrderItem')
Product = apps.get_model('backend', 'ProductReview')


class OrderSummary(ListView):
    model = Order
    template_name = 'com/cart.html'
    context_object_name = 'items'

    def get_queryset(self):
        order = Order.objects.filter(user=self.request.user, ordered=False)
        if order.exists():
            return order[0]

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(OrderSummary, self).dispatch(request, *args, **kwargs)


@login_required(login_url='/accounts/login/')
def add_to_cart(request, p_link):
    link = request.GET.get('url')
    item = get_object_or_404(Product, p_link=p_link)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.item.filter(item__p_link=item.p_link).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Item Updated to cart")
        else:
            messages.info(request, "This item was added to your cart")
            order.item.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.item.add(order_item)
        messages.info(request, "This Item was added to your cart")

    if link:
        # TODO : reverse to cart
        return HttpResponseRedirect(redirect_to=link)
    #  TODO : reverse to product detail
    return HttpResponseRedirect(reverse('beauty:pro-detail', kwargs={'p_link': link}))


@login_required(login_url='/accounts/login/')
def remove_from_cart(request, p_link):
    url = request.GET.get('url')
    item = get_object_or_404(Product, p_link=p_link)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs.first()
        if order.item.filter(item__p_link=item.p_link).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)
            order.item.remove(order_item)
            order_item.delete()
            messages.info(request, "The Item was removed from your cart")
        else:
            messages.info(request, "This item was not in your cart")
    else:
        messages.info(request, "You dont have an active order")

    if url:
        # TODO : redirect to cart
        return HttpResponseRedirect(redirect_to=url)
    # TODO : redirect to item
    return HttpResponseRedirect(reverse('beauty:pro-detail', kwargs={'p_link': p_link}))
