from django.contrib.sitemaps import Sitemap
from .models import *


class PostSitemaps(Sitemap):
    changefreq = 'always'
    priority = 1

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.date_update


class ProductsSitemaps(Sitemap):
    changefreq = 'always'
    priority = 1

    def items(self):
        return ProductReview.objects.all()

    def lastmod(self, obj):
        return obj.p_date_update


