from django.shortcuts import render
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin

Product = 'backend.ProductReview'


class ProductList(ListView):
    model = Product
    template_name = 'core/home.html'
    ordering = ['-pk']
    paginate_by = 10
    context_object_name = 'products'


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

