from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name}'

class Func(models.Model):
    name = models.CharField(max_length=50)

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

    categories = models.ManyToManyField(Category, related_name='videos')
    funcs = models.ManyToManyField(Func, related_name='videos')
    experiences = models.ManyToManyField(Experience, related_name='videos')
    jobtypes = models.ManyToManyField(Jobtype, related_name='videos')

    savers = models.ManyToManyField(User, related_name='saved_videos')

    def get_absolute_url(self):
        return reverse('watch', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.title}'
