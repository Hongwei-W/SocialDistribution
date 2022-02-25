from django.urls import path, include
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views
from .views import NewPostView, PostListView, PostDetailView

app_name = 'myapp'
urlpatterns = [
    # ex: /polls/
    # path('feed/', views.feed, name='feed'),
    path('newpost/', NewPostView.as_view(), name='newpost'),
    path('feed/',PostListView.as_view(), name='postList'),
    path('post/<uuid:pk>',PostDetailView.as_view(), name='postDetail'),
]