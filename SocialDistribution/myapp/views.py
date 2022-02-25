from http.client import HTTPResponse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Post, Comment
from .forms import PostForm, CommentForm

from .forms import LoginForm

# Create your views here.
class PostListView(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-published')
        # form = PostForm()
        context = {
            'postList': posts,
            # 'form': form,
        }
        return render(request,'myapp/feed.html', context)

class NewPostView(View):
    def get(self, request, *args, **kwargs):
        form = PostForm()
        context = {
            'form': form,
        }
        return render(request,'myapp/newpost.html', context)
    
    def post(self, request, *args, **kwargs):
        posts = Post.objects.all()
        form = PostForm(request.POST)

        if form.is_valid():
            newPost = form.save(commit=False)
            # newPost.author = request.user.username
            newPost.save()
        
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

        return render(request, 'myapp/postDetail.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(id=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            newComment = form.save(commit=False)
            # newComment.author = request.user
            newComment.post = post
            newComment.save()

        comments = Comment.objects.filter(post=post).order_by('-published')

        context = {
            'post': post,
            'form': form,
            'comments':comments,
        }

        return render(request, 'myapp/postDetail.html', context)

