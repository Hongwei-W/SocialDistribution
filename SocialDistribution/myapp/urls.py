from django.urls import path

from . import views

app_name = 'myapp'
urlpatterns = [
    # ex: /polls/
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('feed/<str:user_id>/', views.profile, name='profile'),
    path('follow', views.follow, name='follow'),
    #path('feed/<str:user_id>/', views.profile, name='profile'),
    #path('followers_count', views.followers_count, name='followers_count')
    # path('feed/',views.feed, name='feed'),
    path('feed/', views.search),
    path('', views.getuser, name='getuser'),
]

