from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from urllib.parse import urlparse

from .forms import UserForm
from .models import Category, Video

@login_required
def index(request):
    videos = Video.objects.exclude(uploader__groups=request.user.groups.first())
    if 'industry' in request.GET:
        videos = videos.filter(categories__in=request.GET.getlist('industry')).distinct()
    if 'func' in request.GET:
        videos = videos.filter(funcs=request.GET['func'])
        request.user.groups.first()

    context = {
        'videos': videos,
        'group': request.user.groups.first(),
        'industries': Category.objects.all(),
    }
    return render(request, 'main/search.html', context)

@login_required
def search(request):
    video_title = request.GET['title_search']

    videos = Video.objects.exclude(uploader__groups=request.user.groups.first())
    videos = videos.filter(title__icontains=video_title)
    if 'industry' in request.GET:
        videos = videos.filter(categories__in=request.GET.getlist('industry')).distinct()
    if 'func' in request.GET:
        videos = videos.filter(funcs=request.GET['func'])

    context = {
        'videos': videos,
        'group': request.user.groups.first(),
        'industries': Category.objects.all(),
    }
    return render(request, 'main/search.html', context)

def upload(request):
    return render(request, 'main/upload.html')

def account(request):
    uploaded_videos = Video.objects.filter(uploader=request.user)
    saved_videos = Video.objects.filter(savers=request.user)
    context = {
        'uploaded_videos': uploaded_videos,
        'saved_videos': saved_videos,
    }
    return render(request, 'main/account.html', context)

def submit_video(requests):
    #Harvard Django 1:14
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
    return render(request, 'registration/login.html', {'message': None})

# class IndexView(LoginRequiredMixin, ListView):
#     template_name = 'main/recent_uploads.html'
#
#     def get_queryset(self):
#         videos = Video.objects.exclude(uploader__groups=self.request.user.groups.first())
#         if 'industry' in self.request.GET:
#             videos = videos.filter(categories=self.request.GET['industry'])
#         if 'func' in self.request.GET:
#             videos = videos.filter(funcs=self.request.GET['func'])
#         self.videos = videos
#         return videos
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['videos'] = self.videos
#         context['user'] = self.request.user
#         context['group'] = self.request.user.groups.first()
#         context['industries'] = Category.objects.all()
#         return context

class WatchView(DetailView):
    model = Video
    template_name = 'main/watch.html'

    def get_context_data(self, **kwargs):
        previous_url = self.request.META.get('HTTP_REFERER')
        path = urlparse(previous_url).path

        if 'watch' not in path:
            if 'account' in path:
                upnext = Video.objects.filter(savers=self.request.user)
                cache.set('upnext', upnext)
            else:
                query = QueryDict(urlparse(previous_url).query)
                category = query.get('category')
                func = query.get('func')

                upnext = Video.objects.exclude(uploader__groups=self.request.user.groups.first())
                if category is not None:
                    upnext = upnext.filter(categories=category)
                if func is not None:
                    upnext = upnext.filter(funcs=func)
                cache.set('upnext', upnext)

        upnext = cache.get('upnext').exclude(pk=self.kwargs['pk'])
        cache.set('upnext', upnext)

        context = super().get_context_data(**kwargs)
        context['upnext'] = upnext

        return context

@login_required
def save_video(request):
    video_id = None
    user_id = request.user.id
    if request.method == 'GET':
        video_id = request.GET['video_id']
        Video.objects.get(pk=video_id).savers.add(user_id)
    return HttpResponse(user_id)

class UploadView(CreateView):
    model = Video
    fields = ['title', 'file', 'uploader', 'categories', 'funcs', 'experiences', 'jobtypes']

class VideoEdit(UpdateView):
    model = Video
    fields = ['title', 'file', 'uploader', 'categories', 'funcs', 'experiences', 'jobtypes']

class VideoDelete(DeleteView):
    model = Video
    success_url = reverse_lazy('account')

class UserFormView(View):
    form_class = UserForm
    template_name = 'registration/signup.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            group = form.cleaned_data['group']
            user.set_password(password)
            user.save()
            user.groups.add(group)

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))

        return render(request, self.template_name, {'form': form})
