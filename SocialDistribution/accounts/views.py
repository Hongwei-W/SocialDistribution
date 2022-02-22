from pyexpat.errors import messages
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, render

from accounts.forms import SignUpForm, UserCreationForm


def signup(request):
    if request.user.is_authenticated:
        return redirect('accounts_home')  # TODO: Redirect to account page
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # also log the user in at the same time
            user = form.save()
            login(request,
                  user,
                  backend='django.contrib.auth.backends.ModelsBackend')
            return redirect('accounts_home')  # TODO: Redirect to feed page
    else:
        form = SignUpForm()

    context = {'form': form}
    return render(request, 'registration/signup.html', context)