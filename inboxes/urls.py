from django.urls import path, include
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views
from .views import PostListView, OneToOneView

app_name = 'inboxes'
urlpatterns = [
    path('feed/', PostListView.as_view(), name='postList'),
    path('1to1/', OneToOneView.as_view(), name='1to1'),
]