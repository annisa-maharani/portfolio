from django.shortcuts import render
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q as __
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

Product = 'backend.ProductReview'


class ProductList(ListView):
    model = Product
    template_name = 'core/home.html'
    ordering = ['-pk']
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

    def dispatch(self, request, *args, **kwargs):
        return super(ProductList, self).dispatch(request, *args, **kwargs)


class CreateProductView(CreateView, LoginRequiredMixin):
    model = Product
    form_class = None
    template_name = None

    def get_success_url(self):
        return

    def form_valid(self, form):
        return super(CreateProductView, self).form_valid(form)


class UpdateProductView(UpdateView):
    form_class = None
    model = Product
    template_name = None
    query_pk_and_slug = True
    slug_field = 'p_link'
    slug_url_kwarg = 'p_link'

    def get_success_url(self):
        return

    def form_valid(self, form):
        return super(UpdateProductView, self).form_valid(form)


class DeleteProductView(DeleteView):
    model = Product
    template_name = None
    query_pk_and_slug = True
    slug_field = 'p_link'
    slug_url_kwarg = 'p_link'

    def get_success_url(self):
        return

