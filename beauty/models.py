from django.db import models
from backend.models import Post, ProductReview
from ckeditor.fields import RichTextField


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