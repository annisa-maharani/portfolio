from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.conf import settings
import os
from os import remove, path


class MediaIcon(models.Model):
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class SocialMedia(models.Model):
    social = models.ForeignKey(MediaIcon, on_delete=models.CASCADE, related_name='ico')
    redirect = models.CharField(max_length=255, verbose_name="Link Social Media Kamu ")

    def __str__(self):
        return self.social.name


class Profile(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nama Kamu  ")
    nick_name = models.CharField(max_length=255, default="Annisa Maharani", verbose_name="Nama Panggilan")
    desc = RichTextField(verbose_name="Deskripsi Singkat Tentang Kamu : ")
    profile_img = models.ImageField(upload_to='profile', verbose_name="Foto Profil ")
    social_media = models.ManyToManyField(SocialMedia, blank=True, verbose_name="Shared Social Media : ")

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name="Judul Posting  ")
    link = models.SlugField(max_length=255, unique=True, default='')
    content = RichTextField(verbose_name="Konten ")
    desc = models.TextField(verbose_name="Deskripsi Singkat ")
    keyword = models.TextField(verbose_name="keyword pencarian ")
    date_create = models.DateField(auto_now=True)
    date_update = models.DateField(auto_now_add=True)
    likes = models.IntegerField(default=0, verbose_name='likes')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('beauty:detail', args=[self.link])


class MediaManager(models.Model):
    file = models.FileField(upload_to='manager/')

    def __str__(self):
        return str(self.file)

    def filename(self):
        return path.basename(self.file.name)

    def delete(self, using=None, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.file.name))
        super().delete(*args, **kwargs)


class ProductReview(models.Model):
    p_title = models.CharField(max_length=255, verbose_name='Nama Produk')
    p_img = models.FileField(upload_to='product/img/', verbose_name='Link Gambar Produk', default='', max_length=255)
    price = models.FloatField(verbose_name='Harga asli produk : ')
    discount = models.FloatField(verbose_name='Harga yang akan di jual <small> *optional </small>: ', null=True, blank=True)
    p_link = models.SlugField(max_length=255, unique=True)
    p_content = RichTextField(verbose_name='Content')
    p_desc = models.TextField(verbose_name='Simple Description')
    p_keyword = models.TextField(verbose_name='keyword')
    p_date_create = models.DateField(auto_now=True)
    p_date_update = models.DateField(auto_now_add=True)
    p_likes = models.IntegerField(default=0, verbose_name='likes')
    in_stock = models.BooleanField(default=True)

    def contents(self):
        return self.p_content[:50]

    def __str__(self):
        return f"{self.p_title} about {self.p_content[:60]} see more "

    def get_absolute_url(self):
        return reverse('beauty:pro-detail', args=[self.p_link])

    def get_item_add_to_cart(self):
        return reverse('com:add-to-cart', kwargs={'p_link': self.p_link})

    def get_item_remove_from_cart(self):
        return reverse('com:remove-from-cart', kwargs={'p_link': self.p_link})

    def get_reduce_item(self):
        return reverse('com:reduce-item', kwargs={'p_link': self.p_link})

    def filename(self):
        return path.basename(self.p_img.name)

    def delete(self, using=None, *args, **kwargs):
        remove(path.join(settings.MEDIA_ROOT, self.p_img.name))
        super().delete(*args, **kwargs)

