from http.client import HTTPResponse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Post, Comment, Inbox
from .forms import PostForm, CommentForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Author, Post, FollowerCount
from django.views import View
from django.contrib.auth.models import User, auth
from ast import Delete
import re
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy

# Create your views here.
class PostListView(View):
    def get(self, request, *args, **kwargs):
        # posts = Post.objects.all().order_by('-published')
        posts = Inbox.objects.filter(author_id=request.user.username)[0].items
        # form = PostForm()
        context = {
            'postList': posts,
            # 'form': form,
        }
        return render(request,'feed.html', context)

class NewPostView(View):
    def get(self, request, *args, **kwargs):
        form = PostForm()
        context = {
            'form': form,
        }
        return render(request,'newpost.html', context)
    
    def post(self, request, *args, **kwargs):
        posts = Post.objects.all()
        form = PostForm(request.POST)

        if form.is_valid():
            newPost = form.save(commit=False)
            newPost.author = Author.objects.get(id=request.user.username)
            newPost.save()
            Inbox.objects.filter(author_id=request.user.username)[0].items.add(newPost)
            followersID = FollowerCount.objects.filter(user=request.user.username)
            for followerID in followersID:
                Inbox.objects.filter(author_id=followerID.follower)[0].items.add(newPost)
        
        # posts = Post.objects.all()
        # context = {
        #     'postList': posts,
        #     # 'form': form,
        # }
        # return render(request,'myapp/newpost.html', context)
        return redirect('myapp:postList')


class PostDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(id=pk)
        form = CommentForm()
        comments = Comment.objects.filter(post=post).order_by('-published')

        context = {
            'post': post,
            'form': form,
            'comments':comments,
        }

        return render(request, 'postDetail.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(id=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            newComment = form.save(commit=False)
            newComment.author = Author.objects.get(id=request.user.username)
            newComment.post = post
            newComment.save()
            post.count += 1
            post.save()

        comments = Comment.objects.filter(post=post).order_by('-published')

        context = {
            'post': post,
            'form': form,
            'comments':comments,
        }

        return render(request, 'postDetail.html', context)

def profile(request, user_id):
    print("------user id: ", user_id)
    current_author_info = get_object_or_404(Author, pk=user_id)
    follower = request.user.username
    user = user_id

    github_username = current_author_info.github.split("/")[-1]

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
        'github_username': github_username
        }

    return render(request, 'profile.html', context)

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


def search(request):
    author_list = Author.objects.all()
    return render(request, 'feed.html', {'author_list':author_list})

def getuser(request):
    username = request.GET['username']
    # current_author_info = Author.objects.get(displayName = username)
    current_author_info = get_object_or_404(Author, displayName = username)
    user_id = current_author_info.id
    return redirect('/myapp/feed/' + user_id)

class PostEditView(UpdateView):
    model = Post
    fields = ['title','description','visibility']
    template_name = 'postEdit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('myapp:postDetail', kwargs={'pk':pk})

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'postDelete.html'
    success_url = reverse_lazy('myapp:postList')