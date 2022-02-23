from django.urls import path

from . import views
from .views import NewPostView, PostListView, PostDetailView

app_name = 'myapp'
urlpatterns = [
    # ex: /polls/
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    # path('feed/', views.feed, name='feed'),
    path('newpost/', NewPostView.as_view(), name='newpost'),
    path('feed/',PostListView.as_view(), name='postList'),
    path('post/<uuid:pk>',PostDetailView.as_view(), name='postDetail'),

]