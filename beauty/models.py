from os import path, remove
from django.db import models
from backend.models import Post, ProductReview
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.conf import settings


class Subscriber(models.Model):
    email = models.EmailField(max_length=255)
    n_phone = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} with email {self.email}"


class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(null=True, blank=True, max_length=255, default='')
    comment = RichTextField(config_name='comment')

    def __str__(self):
        return f"{self.name} comments at {self.post.title}"


class ProductComment(models.Model):
    product = models.ForeignKey(ProductReview, on_delete=models.CASCADE)
    name = models.CharField(null=True, blank=True, max_length=255, default='')
    comment = RichTextField(config_name='comment')

    def __str__(self):
        return f"{self.name} comments on {self.product.p_title}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile/', null=True, blank=True)
    phone = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username

    def delete(self, using=None, *args, **kwargs):
        remove(path.join(settings.MEDIA_ROOOT, self.image.name))
        super(UserProfile, self).delete(*args, **kwargs)
