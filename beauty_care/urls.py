"""beauty_care URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.contrib.sitemaps.views import sitemap
from backend.sitemaps import PostSitemaps, ProductsSitemaps


sitemaps = {
    'post': PostSitemaps,
    'product': ProductsSitemaps
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='api')),
    path('download/<path>', serve, settings.MEDIA_ROOT),
    path('accounts/', include('allauth.urls')),
    path('order/', include('commerce.urls', namespace='com')),
    path('static/<path>', serve, settings.STATIC_ROOT),
    path('media/<path>', serve, settings.MEDIA_ROOT),
    path('wpcp-admin/', include('backend.urls', namespace="my")),
    path('robots.txt', include('robots.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]

if not settings.DEBUG or settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [path('', include('beauty.urls', namespace='beauty'))]
