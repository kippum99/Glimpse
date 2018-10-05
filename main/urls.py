from django.urls import path, include, re_path
from . import views

urlpatterns = [
    #path('', views.IndexView.as_view(), name='index'),
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    #path('upload', views.upload, name='upload'),
    path('upload', views.UploadView.as_view(), name='upload'),
    path('edit/<int:pk>', views.VideoEdit.as_view(), name='edit'),
    path('delete/<int:pk>', views.VideoDelete.as_view(), name='delete'),
    path('account', views.account, name='account'),
    path('watch/<int:pk>', views.WatchView.as_view(), name='watch'),
    re_path(r'^save_video/$', views.save_video, name='save_video'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout', views.logout_view, name='logout'),
    path('signup', views.UserFormView.as_view(), name='signup'),
]
