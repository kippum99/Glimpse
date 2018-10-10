from django.contrib import admin
from .models import Category, Experience, Jobtype, Tribal, Video, VideoAdmin, Jobseeker, Employer, User

admin.site.register(Category)
admin.site.register(Experience)
admin.site.register(Jobtype)
admin.site.register(Tribal)
admin.site.register(Video, VideoAdmin)
admin.site.register(Jobseeker)
admin.site.register(Employer)
admin.site.register(User)
