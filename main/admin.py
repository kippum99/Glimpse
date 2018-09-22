from django.contrib import admin

from .models import Category, Func, Video

admin.site.register(Category)
admin.site.register(Func)
admin.site.register(Video)
