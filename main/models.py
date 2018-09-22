from django.db import models
from django.urls import reverse

class Video(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(null=True)

    def get_absolute_url(self):
        return reverse('watch', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.title}'

class Category(models.Model):
    name = models.CharField(max_length=30)
    videos = models.ManyToManyField(Video, related_name='categories')

    def __str__(self):
        return f'{self.name}'

class Func(models.Model):
    name = models.CharField(max_length=30)
    videos = models.ManyToManyField(Video, related_name='funcs')
