from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from localflavor.us.models import USStateField
from django.db import models
from django.urls import reverse

class User(AbstractUser):
    is_js = models.BooleanField(default=False)
    is_emp = models.BooleanField(default=False)

class Tribal(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name}'

class Jobseeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    tribals = models.ManyToManyField(Tribal)

class Category(models.Model):
    name = models.CharField(max_length=50)
    techrole = models.BooleanField(null=True)

    def __str__(self):
        return f'{self.name}'

class Experience(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name}'

class Jobtype(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name}'

class Video(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(null=True)
    uploader = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='uploaded_videos')

    jobtypes = models.ManyToManyField(Jobtype, related_name='videos')
    tribals = models.ManyToManyField(Tribal)
    city = models.CharField(max_length=20, null=True)
    state = USStateField(null=True)
    remote = models.BooleanField(default=False)

    role = models.CharField(max_length=1, choices=(('T', 'Tech'), ('M', 'MBA / Management')))

    categories = models.ManyToManyField(Category, related_name='videos')
    experiences = models.ManyToManyField(Experience, related_name='videos')

    savers = models.ManyToManyField(User, related_name='saved_videos')
    submitted_videos1 = models.ManyToManyField('self', related_name='submitted_too', symmetrical=False)
    submitted_videos = models.ManyToManyField('self', related_name='submitted_to', symmetrical=False, through='Submission')

    def get_absolute_url(self):
        return reverse('watch', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.title}'

class Submission(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='video')
    submitted_video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='submitted_video')
    date_submitted = models.DateField()


class SubmissionInline(admin.TabularInline):
    model = Submission
    fk_name = 'video'

class VideoAdmin(admin.ModelAdmin):
    inlines=(SubmissionInline,)
