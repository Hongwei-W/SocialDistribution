from ast import Delete
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Author, Post, FollowerCount
from django.views import View
from django.contrib.auth.models import User, auth

# Create your views here.
def login(request):
    return HttpResponse("You're looking at login page.")
    # render(request, 'myapp/login.html')
def signup(request):
    return HttpResponse("You're looking at signup page.")
    # render(request, 'myapp/signup.html')
def feed(request):
    # return HttpResponse("You're looking at feed page.")
    return render(request, 'myapp/feed.html')

# def profile(request, pk):
#     # user_object = User.objects.get(username=pk)
#     # user_profile = Profile.objects.get(user=user_object)
#     return render(request, 'myapp/profile.html')

def profile(request, user_id):
    print("------user id: ", user_id)
    current_author_info = get_object_or_404(Author, pk=user_id)
    follower = request.user.username
    user = user_id

    if FollowerCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'
    count_followers = len(FollowerCount.objects.filter(user=user_id))
    count_following = len(FollowerCount.objects.filter(follower=user_id))
    context = {
        'current_author_info': current_author_info,
        'button_text': button_text,
        'count_followers': count_followers,
        'count_following': count_following,
        }

    return render(request, 'myapp/profile.html', context)

def follow(request):
    print("follow is working")
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']
        # why user is empty?
        print("!!!!!!!!!______", "request.POST: ", request.POST, "user: ", user, "follower: ", follower)
        if FollowerCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowerCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/myapp/feed/'+user)
        else:
            new_follower = FollowerCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/myapp/feed/'+user)
    else:
        return redirect('/')



# def display_image(request, user_id):
#     current_author_info = get_object_or_404(Author, pk=user_id)
#     avatar = {'avatar': current_author_info.profileImage}