from django.urls import path

from . import views

app_name = 'myapp'
urlpatterns = [
    # ex: /polls/
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('feed/', views.feed, name='feed'),

]