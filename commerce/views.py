from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import *
from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .forms import CheckoutForm
from django.conf import settings
import stripe, datetime
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY

Order = apps.get_model('core', 'Order')
OrderItem = apps.get_model('core', 'OrderItem')
Product = apps.get_model('backend', 'ProductReview')
Address = apps.get_model('beauty', 'Address')


class OrderSummary(ListView):
    model = Order
    template_name = 'com/cart.html'
    context_object_name = 'items'

    def get_queryset(self):
        order = Order.objects.all()
        order = order.filter(user=self.request.user, ordered=False)
        if order.exists():
            return order.first()

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(OrderSummary, self).dispatch(request, *args, **kwargs)


class CheckoutView(View, LoginRequiredMixin):
    def get(self, *args, **kwargs):
        try:
            form = CheckoutForm()
            address = Address.objects.filter(user=self.request.user)

            context = {
                'form': form,
                'address': address
            }
            return render(self.request, 'com/checkout.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You dont have an active order! ")
            return redirect('com:order')

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                payment = form.cleaned_data['payment_option']

                address = self.request.POST.get('address')
                if not address:
                    messages.info(self.request, "You dont Choices the address!")
                    return redirect('com:checkout')
                address = Address.objects.get(address_link=address)

                order.address__address_link = address
                order.save()

                if payment == "S":
                    # TODO : reverse to stripe payment
                    return HttpResponseRedirect(reverse('com:payment', kwargs={'method':'stripe'}))
                elif payment == 'P':
                    # TODO  : reverse to paypal payment
                    return HttpResponseRedirect(reverse('com:payment', kwargs={'method': 'paypal'}))
                else:
                    messages.error(self.request, "Invalid Payment Options ! ")
                    # TODO : redirect to this view (get)
                    return redirect('com:checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, 'You dont have an active order!')
            return redirect('/')

        messages.warning(self.request, "Checkout Failed! ")
        return redirect('com:order')


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'order': order,
            'uri': self.request.build_absolute_uri()
        }
        return render(self.request, 'com/pay/payment.html', context)

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        amount = int(order.get_total())

        host = self.request.get_host()

        success_url = f"http://{host}{reverse('com:payment-success')}"
        cancel_url = f"http://{host}{reverse('com:payment-cancel')}"

        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price_data': {
                        'currency':'idr',
                        'unit_amount': amount * 100,
                        'product_data': {
                            'name': f"Billing For ",
                        }
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
        )
        # if checkout_session.url == success_url:
        if checkout_session.url == checkout_session.success_url:
            print('hai')
        return redirect(checkout_session.url, code=303)


class PaymentSuccess(View):
    template_name = 'com/pay/success.html'

    def get(self, *args, **kwargs):
        now = datetime.date.today()
        order = Order.objects.filter(user=self.request.user, ordered=False)
        if order.exists():
            order = order[0]
            order.ordered = True
            order.paid_at = now
            order.save()

        order = Order.objects.get(user=self.request.user, ordered=True, paid_at=timezone.localtime(timezone.now()).date())
        context = {
            'order': order,
        }
        return render(self.request, self.template_name, context)


class PaymentCancel(TemplateView, LoginRequiredMixin):
    template_name = 'com/pay/cancel.html'


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
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False).first()
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


@login_required(login_url='/accounts/login/')
def reduce_item(request, p_link):
    item = get_object_or_404(Product, p_link=p_link)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.item.filter(item__p_link=item.p_link).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            if order_item.quantity == 1:
                return redirect(f"/remove-from-cart/{p_link}?url=/order/")
            order_item.quantity -= 1
            order_item.save()
            messages.info(request, "This item was reduced from your cart")
        else:
            messages.info(request, "This item was not in your cart")
    else:
        messages.info(request, "You dont have an active order")

    return redirect('/order/')


@csrf_exempt
def stripe_webhook(request):
    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_KEY
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
    # ... handle other event types
    else:
        print('Unhandled event type {}'.format(event['type']))
    # Passed signature verification
    return HttpResponse(status=200)
