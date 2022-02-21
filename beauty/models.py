from os import path, remove
from django.db import models
from backend.models import Post, ProductReview
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.conf import settings

mark = [
    ('R', "Rumah"),
    ('K', "Kantor")
]


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


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_link = models.SlugField(max_length=255)
    post_code = models.CharField(max_length=255)
    main_address = models.TextField()
    detailed_address = models.CharField(max_length=255)
    default = models.BooleanField(default=False)
    mark_as = models.CharField(default='R', choices=mark, max_length=10)

    def __str__(self):
        if self.default:
            return f"{self.user}'s main address"
        return f"{self.user}'s address"

    def address_name(self):
        length = len(str(self.detailed_address)) // 2
        if self.default:
            return f"{self.detailed_address[:length]} - main address"
        return f"{self.detailed_address[:length]}"
