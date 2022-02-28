from pyexpat.errors import messages
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, render

from accounts.forms import SignUpForm, UserCreationForm
from myapp.models import Author


def signup(request):
    # if request.user.is_authenticated:
    #     return redirect('myapp/postList')  # TODO: Redirect to account page
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # user need to go back to log in
            form.save()
            user = form.save()
            # login(request, user, backend='django.contrib.auth.backends.ModelsBackend')
            author = Author(id=user.username, host="http://127.0.0.1:5454/", displayName=user.username)
            author.save()
            return redirect('login')
    else:
        form = SignUpForm()

    context = {'form': form}
    return render(request, 'registration/signup.html', context)
