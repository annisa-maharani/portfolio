from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import *
from backend.models import Profile, Post, ProductReview
from .forms import *
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Q as __
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .utils import link_generator, address_default
from django.contrib import messages
links = 'link'
p_links = 'p_link'


class MainPage(TemplateView):
    template_name = 'beauty/main.html'

    def get_context_data(self, **kwargs):
        context = super(MainPage, self).get_context_data(**kwargs)
        profile = get_object_or_404(Profile, pk=1)
        latest = Post.objects.all()[:3]
        pro_latest = ProductReview.objects.all()[:3]

        context['products'] = pro_latest
        context['profile'] = profile
        context['latest'] = latest
        return context


class AddAddressView(View):
    model = Address
    template_name = 'beauty/forms.html'
    form_class = AddAddressForm

    def get(self, *args, **kwargs):
        context = {
            'form': self.form_class
        }
        return render(self.request, self.template_name, context)
    
    def post(self, *args, **kwargs):
        url = self.request.GET.get('url')
        form = self.form_class(self.request.POST or None)
        if form.is_valid():
            link = link_generator(12)
            address = Address.objects.all()
            add_link = [x.address_link for x in address]

            while True:
                if link in add_link:
                    link = link_generator(12)
                else:
                    break

            default = address_default(self.request)
            if not default:
                form.instance.default = True

            form.instance.address_link = link
            form.instance.user = self.request.user
            form.save()

        return redirect(url) if url and url is not None else redirect('beauty:profile')

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(AddAddressView, self).dispatch(request, *args, **kwargs)


class UpdateAddress(UpdateView):
    model = Address
    template_name = 'beauty/forms.html'
    form_class = None


class AddSubscriber(CreateView):
    model = Subscriber
    form_class = AddSubscriberForm
    template_name = 'beauty/sub.html'


class PageDetail(DetailView):
    model = Post
    template_name = 'beauty/detail.html'
    context_object_name = 'post'
    query_pk_and_slug = True
    slug_field = links
    slug_url_kwarg = links

    def get_context_data(self, **kwargs):
        context = super(PageDetail, self).get_context_data(**kwargs)
        form = AddCommentForm
        this = get_object_or_404(Post, link=self.kwargs[links])
        comments = PostComment.objects.filter(post=this)
        pro_post = True

        context['form'] = form
        context['pro_post'] = pro_post
        context['comments'] = comments
        return context


class PageListView(ListView):
    model = Post
    context_object_name = 'post'
    template_name = 'beauty/list.html'
    ordering = '-id'
    paginate_by = 5

    def get_queryset(self):
        q = self.request.GET.get('q')
        post = Post.objects.all()
        if q is not None:
            post = Post.objects.filter(
                __(title__icontains=q) | __(content__icontains=q) |
                __(desc__icontains=q) | __(keyword__icontains=q)
            ).order_by(self.ordering)
            return post
        else:
            return post

    def get_context_data(self, **kwargs):
        context = super(PageListView, self).get_context_data(**kwargs)
        pd = self.request.GET.get('pd')
        if pd is not None:
            if pd == '1':
                desk = True
            else:
                desk = False

        else:
            desk = True

        context['desk'] = desk
        return context


class UpdateProfileView(View):
    def get(self, *args, **kwargs):
        user = self.request.user
        profile = UserProfile.objects.filter(user=user)
        form = UserForm(instance=user)
        e_form = UserProfileForm(instance=profile[0]) if profile.exists() else UserProfileForm()

        context = {
            'form': form,
            'e_form': e_form,
        }

        return render(self.request, 'beauty/pr_form.html', context)

    def post(self, *args, **kwargs):
        user = self.request.user
        form = UserForm(self.request.POST or None, instance=user)
        profile = UserProfile.objects.filter(user=user)
        e_form = UserProfileForm(self.request.POST or None, self.request.POST or None, instance=user) if profile.exists() else UserProfileForm(self.request.POST or None, self.request.FILES or None)

        if form.is_valid() and e_form.is_valid():
            form.save()
            e_form.instance.user = self.request.user
            e_form.save()
            messages.info(self.request, "Profile Updated ! ")
        return redirect('beauty:profile')

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(UpdateProfileView, self).dispatch(request, *args, **kwargs)


class AddComment(CreateView):
    model = PostComment
    form_class = AddCommentForm
    query_pk_and_slug = True
    slug_field = links
    slug_url_kwarg = links

    def get_success_url(self):
        return reverse('beauty:detail', args=[self.kwargs[links]])

    def form_valid(self, form):
        def current_pk():
            comment = PostComment.objects.all().order_by('-id').first()
            if comment is None:
                return 0
            return int(comment.pk)

        if not self.request.POST.get('name'):
            form.instance.name = f"Unknown User{current_pk()}"
        else:
            form.instance.name = self.request.POST.get('name')
        post = get_object_or_404(Post, link=self.kwargs['link'])
        form.instance.post = post
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not self.request.POST.get('comment'):
            return HttpResponseRedirect(reverse('beauty:detail', args=[self.kwargs[links]]))
        return super().dispatch(request, *args, **kwargs)


class ProductDetail(DetailView):
    slug_field = p_links
    slug_url_kwarg = p_links
    query_pk_and_slug = True
    model = ProductReview
    template_name = 'beauty/detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        pew = self.request.GET.get('pp')
        form = AddProductCommentForm
        this = get_object_or_404(ProductReview, p_link=self.kwargs[p_links])
        comments = ProductComment.objects.filter(product_id=this.pk)
        """ pew == 1 post and pew == 2 is products """
        if pew == '1':
            pro_post = True
        else:
            pro_post = False

        context['form'] = form
        context['comments'] = comments
        context['con'] = pro_post
        return context


class CreateProductComment(CreateView):
    model = ProductComment
    query_pk_and_slug = True
    slug_url_kwarg = p_links
    slug_field = p_links
    form_class = AddProductCommentForm

    def get_success_url(self):
        return reverse('beauty:pro-detail', args=[self.kwargs[p_links]])

    def form_valid(self, form):
        def current_pk():
            pro = ProductReview.objects.all().order_by('-id').first()
            if not pro:
                return 0
            return int(pro.pk)

        if not self.request.POST.get('name'):
            form.instance.name = f"Unknown User{current_pk()}"
        else:
            form.instance.name = form.cleaned_data['name']
        this = get_object_or_404(ProductReview, p_link=self.kwargs[p_links])
        form.instance.product_id = this.pk
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not self.request.POST.get('comment'):
            return HttpResponseRedirect(reverse('beauty:pro-detail', kwargs={'p_link': self.kwargs[p_links]}))
        return super().dispatch(request, *args, **kwargs)


class ProductList(ListView):
    model = ProductReview
    template_name = 'beauty/list.html'
    ordering = '-id'
    paginate_by = 5
    context_object_name = 'post'

    def get_queryset(self):
        q = self.request.GET.get('q')
        prod = ProductReview.objects.all()
        if q is not None:
            prod = ProductReview.objects.filter(
                __(p_title__icontains=q) | __(p_content__icontains=q) |
                __(p_desc__icontains=q) | __(p_keyword__icontains=q)
            ).order_by(self.ordering)
            return prod
        else:
            return prod

    def get_context_data(self, **kwargs):
        context = super(ProductList, self).get_context_data(**kwargs)
        pd = self.request.GET.get('pd')
        if pd is not None:
            if pd == '1':
                desk = True
            else:
                desk = False
        else:
            desk = False

        context['desk'] = desk
        return context


def add_likes(request, link):
    if request.method == 'POST':
        post = get_object_or_404(Post, link=link)
        if post:
            post.likes += 1
            post.save()
    return HttpResponseRedirect(reverse('beauty:detail', args=[link]))


def pro_likes(request, p_link):
    if request.method == 'POST':
        product = get_object_or_404(ProductReview, p_link=p_link)
        if product:
            product.p_likes += 1
            product.save()
    return HttpResponseRedirect(reverse('beauty:pro-detail', args=[p_link]))


class ProfileView(View):
    def get(self, *args, **kwargs):
        user = self.request.user
        context = None

        return render(self.request, 'beauty/profile.html', context)

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(ProfileView, self).dispatch(request, *args, **kwargs)
