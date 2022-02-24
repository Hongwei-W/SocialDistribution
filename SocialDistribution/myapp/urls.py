from django.urls import path, include
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

app_name = 'myapp'
urlpatterns = [
    # ex: /polls/
    url(r'^login/$', auth_views.LoginView.as_view(template_name='myapp/login.html'), name='login'),
    # url(r'^logout/$', auth_views.logout, name='logout'),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('feed/', views.feed, name='feed'),
    # path('', views.LoginView.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
    path('feed/', views.feed, name='feed'),

]