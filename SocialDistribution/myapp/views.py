from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def login(request):
    render(request, 'myapp/login.html')
def signup(request):
    render(request, 'myapp/signup.html')