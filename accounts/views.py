from django.shortcuts import redirect, render

from accounts.forms import AuthorInfoForm, SignUpForm
from authors.models import Author, Followers
from common.models import ServerSetting
from inboxes.models import Inbox


def signup(request):
    needs_admin_approval = not ServerSetting.objects.first()\
    .allow_independent_user_login

    # if request.user.is_authenticated:
    #     return redirect('myapp:postList')  # TODO: Redirect to account page
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        author_form = AuthorInfoForm(request.POST)
        if form.is_valid() and author_form.is_valid():
            user = form.save()

            if needs_admin_approval:
                user.is_active = False
                user.save()

            try:
                profile_image_string = author_form.cleaned_data['profileImage']
            except:
                profile_image_string = 'https://www.ibm.com/support/pages/system/files/support/swg/rattech.nsf/0/a857b0395de747c085257bcf0037ccb6/Symptom/0.126.gif'

            github = author_form.cleaned_data['github']
            host = request.build_absolute_uri('/')
            author = Author(username=user.username,
                            host=host,
                            displayName=user.username,
                            profileImage=profile_image_string,
                            github=github)

            author.save()
            author.id = author.host + "authors/" + str(author.uuid)
            print("author id is " + author.id)
            author.url = author.id
            author.save()
            inbox = Inbox(author=author)
            inbox.save()
            followers = Followers(user=author)
            followers.save()
            return redirect('/accounts/login')
    else:
        form = SignUpForm()
        author_form = AuthorInfoForm()
    context = {
        'form': form,
        'author_info_form': AuthorInfoForm,
        'needs_admin_approval': needs_admin_approval
    }
    return render(request, 'registration/signup.html', context)
