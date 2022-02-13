from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def login(request):
    return HttpResponse("You're looking at login page.")
    # render(request, 'myapp/login.html')
def signup(request):
    return HttpResponse("You're looking at signup page.")
    # render(request, 'myapp/signup.html')