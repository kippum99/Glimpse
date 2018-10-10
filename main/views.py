from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import redirect

from urllib.parse import urlparse

from .forms import JSVideoForm, EmpVideoForm, JSSignUpForm, EmpSignUpForm
from .models import User, Category, Experience, Jobtype, Tribal, Video

@login_required
def index(request):
    user_is_js = request.user.is_js
    videos = Video.objects.exclude(uploader__is_js=user_is_js)
    if 'category' in request.GET:
        videos = videos.filter(categories__in=request.GET.getlist('category')).distinct()
    if 'tribal' in request.GET:
        videos = videos.filter(tribals__in=request.GET.getlist('tribal')).distinct()
    #if 'func' in request.GET:
    #     videos = videos.filter(funcs=request.GET['func'])
    #     request.user.groups.first()
    context = {
        'videos': videos,
        'techs': Category.objects.filter(techrole=1),
        'mbas': Category.objects.filter(techrole=0),
        'tribals': Tribal.objects.all(),
        'jobtypes': Jobtype.objects.all(),
        'experiences': Experience.objects.all(),
    }
    return render(request, 'main/search.html', context)

@login_required
def search(request):
    video_title = request.GET['title_search']

    videos = Video.objects.all()
    #videos = Video.objects.exclude(uploader__groups=request.user.groups.first())
    videos = videos.filter(title__icontains=video_title)
    if 'category' in request.GET:
        videos = videos.filter(categories__in=request.GET.getlist('category')).distinct()
    if 'func' in request.GET:
        videos = videos.filter(funcs=request.GET['func'])

    context = {
        'videos': videos,
        #'group': request.user.groups.first(),
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

def signup_view(request):
    return render(request, 'registration/signup.html')

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
                #func = quer.

                user_is_js = self.request.user.is_js
                upnext = Video.objects.exclude(uploader__is_js=user_is_js)

                if category is not None:
                    upnext = upnext.filter(categories=category)
                # if func is not None:
                #     upnext = upnext.filter(funcs=func)
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
    return HttpResponse()

@login_required
def submit_my_video(request):
    context = {
        'videos': Video.objects.filter(uploader=request.user)
    }
    return render(request, 'main/submit_video.html', context)

@login_required
def submit_video(request):
    if request.method == 'POST':
        video = Video.objects.get(pk=request.POST.get('video'))
        submit_to = Video.objects.get(pk=request.POST.get('submit_to'))
        submit_to.submitted_videos.add(video)
    return HttpResponse()

# class UploadView(CreateView):
#     model = Video
#     fields = ['title', 'file', 'uploader', 'categories', 'experiences', 'jobtypes']

class UploadView(CreateView):
    form_class = JSVideoForm
    template_name = 'main/upload_js.html'

    def get(self, request):
        if request.user.is_js: #if user is job seeker
            self.form_class = JSVideoForm
            self.template_name = 'main/upload_js.html'
        elif request.user.is_emp: # if user is employer
            self.form_class = EmpVideoForm
            self.template_name = 'main/upload_emp.html'
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
        form.instance.uploader = self.request.user
        return super().form_valid(form)

class VideoEdit(UpdateView):
    model = Video
    fields = ['title', 'file', 'uploader', 'categories', 'funcs', 'experiences', 'jobtypes']

class VideoDelete(DeleteView):
    model = Video
    success_url = reverse_lazy('account')

class JSSignUpView(CreateView):
    model = User
    form_class = JSSignUpForm
    template_name = 'registration/signup_js.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')

class EmpSignUpView(CreateView):
    model = User
    form_class = EmpSignUpForm
    template_name = 'registration/signup_emp.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')

# class UserFormView(View):
#     form_class = UserForm
#     template_name = 'registration/signup.html'
#
#     def get(self, request):
#         form = self.form_class(None)
#         return render(request, self.template_name, {'form': form})
#
#     def post(self, request):
#         form = self.form_class(request.POST)
#
#         if form.is_valid():
#             user = form.save(commit=False)
#
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             group = form.cleaned_data['group']
#             user.set_password(password)
#             user.save()
#             user.groups.add(group)
#
#             user = authenticate(username=username, password=password)
#
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponseRedirect(reverse('index'))
#
#         return render(request, self.template_name, {'form': form})
