from http.client import HTTPResponse
from django.http import HttpResponse
from django.shortcuts import render

from .forms import LoginForm

# Create your views here.
# def login(request):
#     # return HttpResponse("You're looking at login page.")
#     if request.method == 'POST':
#         form = LoginForm(request.POST)

#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             return HTTPResponse(str(username + password))
#     else:
#         form = LoginForm()

#     return render(request, 'myapp/login.html', {'form': form})

def signup(request):
    return HttpResponse("You're looking at signup page.")
    # render(request, 'myapp/signup.html')

def feed(request):
    return HttpResponse("Feed") 