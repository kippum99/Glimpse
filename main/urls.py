from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('search', views.search, name='search'),
    path('upload', views.upload, name='upload'),
    path('account', views.account, name='account'),
    path('watch', views.watch, name='watch2'),
    path('watch/<int:pk>', views.WatchView.as_view(), name='watch'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout', views.logout_view, name='logout'),
]
