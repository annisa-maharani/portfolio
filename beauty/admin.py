from django.contrib import admin
from .models import Subscriber, PostComment, ProductComment

admin.site.register(Subscriber)
admin.site.register(PostComment)
admin.site.register(ProductComment)
