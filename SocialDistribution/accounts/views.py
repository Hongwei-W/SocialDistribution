from pyexpat.errors import messages
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, render

from accounts.forms import AuthorInfoForm, SignUpForm, UserCreationForm
from myapp.models import Author, Inbox


def signup(request):
    if request.user.is_authenticated:
        return redirect('myapp:postList')  # TODO: Redirect to account page
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        author_form = AuthorInfoForm(request.POST)
        if form.is_valid():
            # user need to go back to log in
            form.save()
            user = form.save()
            author_form_valid = author_form.is_valid()
            breakpoint()
            if author_form_valid:
                try:
                    author = Author(
                        id=user.username,
                        host="http://127.0.0.1:5454/",
                        displayName=user.username,
                        profileImage=author_form.cleaned_data['profileImage'])
                except Exception:
                    author = Author(
                        id=user.username,
                        host="http://127.0.0.1:5454/",
                        displayName=user.username,
                        profileImage=
                        "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.jotform.com%2Fanswers%2F2036354-account-verify-email-invalid-link-error&psig=AOvVaw29n4Gez3oJoT7AQkM97mSR&ust=1646438612991000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCIiCxPiTq_YCFQAAAAAdAAAAABAD"
                    )
            else:
                author = Author(id=user.username,
                                host="http://127.0.0.1:5454/",
                                displayName=user.username,
                                profileImage="no image selected")
            author.save()
            # inbox = Inbox(author=author)
            # inbox.save()
            return redirect('login')
    else:
        form = SignUpForm()
        author_form = AuthorInfoForm()
    context = {'form': form, 'author_info_form': AuthorInfoForm}
    return render(request, 'registration/signup.html', context)

