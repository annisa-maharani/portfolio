from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse


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
        return reverse('my:update', args=[self.link])


class MediaManager(models.Model):
    file = models.FileField(upload_to='manager/')

    def __str__(self):
        return str(self.file)

    def delete(self, using=None, keep_parents=False, *args, **kwargs):
        self.delete()
        super().delete(*args, **kwargs)


class ProductReview(models.Model):
    p_title = models.CharField(max_length=255, verbose_name='Nama Produk')
    p_img = models.CharField(verbose_name='Link Gambar Produk', default='', max_length=255)
    p_link = models.SlugField(max_length=255, unique=True)
    p_content = RichTextField(verbose_name='Content')
    p_desc = models.TextField(verbose_name='Simple Description')
    p_keyword = models.TextField(verbose_name='keyword')
    p_date_create = models.DateField(auto_now=True)
    p_date_update = models.DateField(auto_now_add=True)
    p_likes = models.IntegerField(default=0, verbose_name='likes')

    def __str__(self):
        return f"{self.p_title} about {self.p_content[:60]} see more "