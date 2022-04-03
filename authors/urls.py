from django.urls import path

from . import views

app_name = 'authors'
urlpatterns = [
    # ex: /polls/
    path('authors/<str:user_id>', views.profile, name='profile'),
    path('follow', views.follow, name='follow'),
    path('friendRequests', views.friendRequests, name='friendRequests'),
    path('acceptFriendRequest/<actor_id>', views.acceptFriendRequest, name='acceptFriendRequest'),
    path('', views.getuser, name='getuser'),
    path('authors/edit/<str:user_id>', views.editProfile, name='editProfile'),
]