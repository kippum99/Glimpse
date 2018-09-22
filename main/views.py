from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Video

def search(request):
    video_title = request.GET['title_search']
    videos = Video.objects.filter(title__icontains=video_title)
    if 'category' in request.GET:
        videos = videos.filter(categories=request.GET['category'])
    if 'func' in request.GET:
        videos = videos.filter(funcs=request.GET['func'])

    context = {
        'videos': videos
    }
    return render(request, 'main/search.html', context)

def upload(request):
    return render(request, 'main/upload.html')

def account(request):
    return render(request, 'main/account.html')

def watch(request):
    return render(request, 'main/watch.html')

def submit_video(requests):
    #Django 1:14
    return

def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'main/login.html', {'message': 'Invalid credentials'})

def logout_view(request):
    logout(request)
    return render(request, 'main/login.html', {'message': None})

class IndexView(LoginRequiredMixin, ListView):
    template_name = 'main/recent_uploads.html'

    def get_queryset(self):
        videos = Video.objects.all()
        if 'category' in self.request.GET:
            videos = videos.filter(categories=self.request.GET['category'])
        if 'func' in self.request.GET:
            videos = videos.filter(funcs=self.request.GET['func'])
        self.videos = videos
        return videos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['videos'] = self.videos
        context['user'] = self.request.user
        context['group'] = self.request.user.groups.first()
        return context

class WatchView(DetailView):
    model = Video
    template_name = 'main/watch.html'
