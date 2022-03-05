from django.shortcuts import get_object_or_404, render
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q as __
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from .forms import *
from .utils import code_generator, link_generator, b_url, staff_required
from django.http import HttpResponseRedirect
from .models import Order

p_link = 'p_link'


class ProductList(ListView):
    model = Product
    template_name = 'be/products.html'
    ordering = '-pk'
    paginate_by = 10
    context_object_name = 'products'

    def get_queryset(self):
        q = self.request.GET.get('q')
        pro = Product.objects.all()
        if q is not None:
            pro = pro.filter(
                __(p_title__icontains=q) | __(p_content__icontains=q) |
                __(p_keyword__icontains=q) | __(p_desc__icontains=q)
            ).order_by(self.ordering)
        else:
            pro = pro.order_by(self.ordering)
        return pro

    @method_decorator(login_required(login_url='accounts/login/'))
    @method_decorator(staff_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductList, self).dispatch(request, *args, **kwargs)


class CreateProductView(CreateView, LoginRequiredMixin):
    model = Product
    form_class = ProductForm
    template_name = 'be/create.html'

    def get_success_url(self):
        return reverse('my:core:products')

    def form_valid(self, form):
        link = form.cleaned_data['p_title']
        link = link_generator(link)

        form.instance.p_link = link
        return super(CreateProductView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        back = self.request.GET.get('b')

        context['back'] = b_url(back)
        return context

    @method_decorator(staff_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CreateProductView, self).dispatch(request, *args, **kwargs)


class UpdateProductView(UpdateView):
    form_class = ProductForm
    model = Product
    template_name = 'be/create.html'
    query_pk_and_slug = True
    slug_field = p_link
    slug_url_kwarg = p_link

    def get_success_url(self):
        return reverse('my:core:update-product', kwargs={'p_link': self.object.p_link})

    def form_valid(self, form):
        link = form.cleaned_data['p_title']
        link = link_generator(link)

        form.instance.p_link = link
        return super(UpdateProductView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UpdateProductView, self).get_context_data(**kwargs)
        back = self.request.GET.get('b')

        context['back'] = b_url(back)
        return context

    @method_decorator(login_required(login_url='/accounts/login/'))
    @method_decorator(staff_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UpdateProductView, self).dispatch(request, *args, **kwargs)


class DeleteProductView(DeleteView, LoginRequiredMixin):
    model = Product
    template_name = 'be/delete.html'
    query_pk_and_slug = True
    slug_field = p_link
    slug_url_kwarg = p_link
    context_object_name = 'post'

    def get_success_url(self):
        return reverse('my:core:products')

    def get_context_data(self, **kwargs):
        context = super(DeleteProductView, self).get_context_data(**kwargs)
        back = self.request.GET.get('b')

        context['back'] = b_url(back)
        return context

    @method_decorator(staff_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DeleteProductView, self).dispatch(request, *args, **kwargs)


class ReviewProductView(DetailView):
    template_name = 'be/preview.html'
    model = Product
    query_pk_and_slug = True
    slug_field = p_link
    slug_url_kwarg = p_link
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(ReviewProductView, self).get_context_data(**kwargs)
        page = False

        context['page'] = page
        return context

    @method_decorator(login_required(login_url='/accounts/login/'))
    @method_decorator(staff_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ReviewProductView, self).dispatch(request, *args, **kwargs)


class OnGoingUserOrderList(ListView):
    model = Order
    context_object_name = 'items'
    template_name = 'core/on_going.html'

    def get_queryset(self):
        return Order.objects.filter(ordered=True)

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class SetShipped(CreateView):
    model = Shipping
    template_name = 'core/forms.html'
    form_class = SetShippingForm
    
    def get_success_url(self):
        return 
    
    def form_valid(self, form):
        order = get_object_or_404(Order, reff=self.kwargs['reff'])
        form.instance.reff = code_generator(14)
        form.instance.order = order
        return super().form_valid(form)
    
    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    