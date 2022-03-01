"""SocialDistribution URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from rest_framework.urlpatterns import format_suffix_patterns

from myapp import views


urlpatterns = [
    #
    #   Accounts
    #
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    #
    #   Feed
    #
    #path('', include('myapp.urls', 'postList')),
    #
    #   Admin
    #
    path('admin/', admin.site.urls),
    path('myapp/', include('myapp.urls')),
    #
    #   API
    #
    path('service/authors/', views.authorsAPI.as_view()),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
