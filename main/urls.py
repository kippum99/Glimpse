from django.urls import path, include, re_path
from . import views

urlpatterns = [
    #path('', views.IndexView.as_view(), name='index'),
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('upload', views.UploadView.as_view(), name='upload'),
    path('edit/<int:pk>', views.VideoEdit.as_view(), name='edit'),
    path('delete/<int:pk>', views.VideoDelete.as_view(), name='delete'),
    path('account', views.account, name='account'),
    path('watch/<int:pk>', views.WatchView.as_view(), name='watch'),
    re_path(r'^save_video/$', views.save_video, name='save_video'),
    path('submit_my_video', views.submit_my_video, name='submit_my_video'),
    path('submit_video', views.submit_video, name='submit_video'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout', views.logout_view, name='logout'),
    path('signup', views.signup_view, name='signup'),
    path('signup/jobseeker', views.JSSignUpView.as_view(), name='js_signup'),
    path('signup/employer', views.EmpSignUpView.as_view(), name='emp_signup'),
]
