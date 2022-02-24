from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from .views import signup

urlpatterns = [
    path('signup/', signup, name='signup'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
]