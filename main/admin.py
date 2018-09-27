from django.contrib import admin

from .models import Category, Experience, Func, Jobtype, Video

admin.site.register(Category)
admin.site.register(Experience)
admin.site.register(Func)
admin.site.register(Jobtype)
admin.site.register(Video)
