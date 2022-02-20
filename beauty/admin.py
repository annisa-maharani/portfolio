from django.contrib import admin
from .models import Subscriber, PostComment, ProductComment, Address, UserProfile

admin.site.register(Subscriber)
admin.site.register(PostComment)
admin.site.register(ProductComment)
admin.site.register(Address)
admin.site.register(UserProfile)
