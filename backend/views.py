from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.views.generic import *
from .forms import *
from .utils import staff_required, slug_generator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


link = 'link'
p_link = 'p_link'


class AdminHome(ListView):
    template_name = "be/home.html"
    model = Post
    context_object_name = 'post'
    ordering = ['-id']
    paginate_by = 10

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(AdminHome, self).dispatch(request, *args, **kwargs)


class CreatePost(CreateView):
    template_name = "be/create.html"
    model = Post
    form_class = CreatePostForm

    def get_success_url(self):
        return reverse('my:update', args=[self.object.link])

    def get_context_data(self, **kwargs):
        context = super(CreatePost, self).get_context_data(**kwargs)
        back = self.request.GET.get('b')

        def b_url():
            if back is not None:
                """ 1 is for post and 2 is for products """
                if back == '1':
                    return True
                else:
                    return False

        context['back'] = b_url()

        return context

    def form_valid(self, form):
        bad_chars = [';', ':', '!', "*", '!', '@', '#', '$', '%', '^', '&', '(', ')']
        _link = form.cleaned_data['title']
        _link = _link.replace(' ', '-')

        for i in bad_chars:
            if bad_chars[-3] in _link:
                _link = _link.replace(i, 'n')
            _link = _link.replace(i, '')

        if _link[-1] == '-':
            _link = _link[:-1]
            if _link[-1] == '-':
                _link = _link[:-1]

        form.instance.link = _link.lower()
        return super().form_valid(form)

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(CreatePost, self).dispatch(request, *args, **kwargs)


class UpdatePost(UpdateView):
    template_name = 'be/update.html'
    model = Post
    form_class = CreatePostForm
    query_pk_and_slug = True
    slug_field = link
    slug_url_kwarg = link

    def get_success_url(self):
        return reverse('my:update', args=[self.object.link])

    def form_valid(self, form):
        bad_chars = [';', ':', '!', "*", '!', '@', '#', '$', '%', '^', '&', '(', ')']
        _link = form.cleaned_data['title']
        _link = _link.replace(' ', '-')

        for i in bad_chars:
            if bad_chars[-3] in _link:
                _link = _link.replace(i, 'n')
            _link = _link.replace(i, '')

        if _link[-1] == '-':
            _link = _link[:-1]
            if _link[-1] == '-':
                _link = _link[:-1]

        form.instance.link = _link.lower()
        return super().form_valid(form)

    @method_decorator(login_required(login_url='/acconts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(UpdatePost, self).dispatch(request, *args, **kwargs)


class DeletePost(DeleteView):
    model = Post
    template_name = "be/delete.html"
    query_pk_and_slug = True
    slug_field = link
    slug_url_kwarg = link

    def get_success_url(self):
        return reverse('my:home')

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(DeletePost, self).dispatch(request, *args, **kwargs)


class MediaManagerView(ListView):
    model = MediaManager
    paginate_by = 10
    template_name = 'be/media.html'
    ordering = ['-id']
    context_object_name = 'media'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MediaManagerView, self).get_context_data(**kwargs)

        return context

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(MediaManagerView, self).dispatch(request, *args, **kwargs)


class MediaUpload(CreateView):
    model = MediaManager
    template_name = 'be/media_upload.html'
    fields = "__all__"

    def get_success_url(self):
        return reverse('my:media-manager')

    def form_valid(self, form):
        form.save(commit=False)
        if self.request.FILES:
            files = self.request.FILES.getlist('file')[:-1]
            for f in files:
                self.model.objects.create(file=f)

        return super().form_valid(form)

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.FILES.getlist('file'):
            return redirect('my:media-manager')
        return super(MediaUpload, self).dispatch(request, *args, **kwargs)


class PreviewPage(DetailView):
    model = Post
    template_name = 'be/preview.html'
    context_object_name = 'post'
    query_pk_and_slug = True
    slug_field = link
    slug_url_kwarg = link

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(PreviewPage, self).dispatch(request, *args, **kwargs)


@login_required(login_url='/accounts/login/')
def MediaUploadTest(request):
    if request.method == 'POST':
        files = request.FILES.getlist('file')
        for file in files:
            print(file)

    return redirect('my:media-manager')


@login_required(login_url='/accounts/login/')
def delete_all_media(request):
    if request.method == 'POST':
        media = MediaManager.objects.all()
        media.delete()
    return redirect("my:media-manager")


""" Profile Editing """


def profile_edit(request):
    profile = get_object_or_404(Profile, pk=1)
    form = UpdateProfileForm(request.POST or None, request.FILES or None, instance=profile)
    if form.is_valid():
        form.save()
        return redirect('my:home')

    context = {
        'form': form,
    }

    return render(request, 'be/create.html', context)


""" Products """


class ProductsList(ListView):
    model = ProductReview
    template_name = 'be/products.html'
    ordering = '-id'
    context_object_name = 'products'

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductsList, self).dispatch(request, *args, **kwargs)


class CreateProducts(CreateView):
    model = ProductReview
    form_class = CreateProductForm
    template_name = 'be/create.html'

    def get_success_url(self):
        return reverse('my:products')

    def form_valid(self, form):
        bad_chars = [';', ':', '!', "*", '!', '@', '#', '$', '%', '^', '&', '(', ')']
        _link = form.cleaned_data['p_title']
        _link = _link.replace(' ', '-')

        for i in bad_chars:
            if bad_chars[-3] in _link:
                _link = _link.replace(i, 'n')
            _link = _link.replace(i, '')

        if _link[-1] == '-':
            _link = _link[:-1]
            if _link[-1] == '-':
                _link = _link[:-1]

        form.instance.p_link = _link.lower()
        return super(CreateProducts, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateProducts, self).get_context_data(**kwargs)
        back = self.request.GET.get('b')

        def b_url():
            if back is not None:
                """ 1 is for post and 2 is for products """
                if back == '1':
                    return True
                else:
                    return False

        context['back'] = b_url()

        return context

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        print(self.request.GET.get('b'))
        return super(CreateProducts, self).dispatch(request, *args, **kwargs)


class UpdateProductPost(UpdateView):
    model = ProductReview
    template_name = 'be/create.html'
    form_class = CreateProductForm
    query_pk_and_slug = True
    slug_field = p_link
    slug_url_kwarg = p_link

    def get_success_url(self):
        return reverse('my:update-product', args=[self.object.p_link])

    def form_valid(self, form):
        bad_chars = [';', ':', '!', "*", '!', '@', '#', '$', '%', '^', '&', '(', ')']
        _link = form.cleaned_data['p_title']
        _link = _link.replace(' ', '-')

        for i in bad_chars:
            if bad_chars[-3] in _link:
                _link = _link.replace(i, 'n')
            _link = _link.replace(i, '')

        if _link[-1] == '-':
            _link = _link[:-1]
            if _link[-1] == '-':
                _link = _link[:-1]

        form.instance.p_link = _link.lower()
        return super(UpdateProductPost, self).form_valid(form)

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(UpdateProductPost, self).dispatch(request, *args, **kwargs)


class DeleteProductPost(DeleteView):
    model = ProductReview
    template_name = 'be/delete.html'
    query_pk_and_slug = True
    slug_field = p_link
    slug_url_kwarg = p_link
    context_object_name = 'post'

    def get_success_url(self):
        return reverse('my:products')

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(DeleteProductPost, self).dispatch(request, *args, **kwargs)


class ReviewProductsPost(DetailView):
    model = ProductReview
    template_name = 'be/preview.html'
    query_pk_and_slug = True
    slug_url_kwarg = p_link
    slug_field = p_link
    context_object_name = 'post'

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(ReviewProductsPost, self).dispatch(request, *args, **kwargs)
