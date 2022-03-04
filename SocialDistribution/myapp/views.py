from http.client import HTTPResponse
from urllib import request
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Post, Comment, Inbox, Like
from .forms import PostForm, CommentForm, ShareForm
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
        context = {
            'postList': posts,
            # 'form': form,
        }
        return render(request,'feed.html', context)

class NewPostView(View):
    def get(self, request, *args, **kwargs):
        form = PostForm()
        share_form = ShareForm()
        context = {
            'form': form,
            'share_form': share_form,
        }
        return render(request,'newpost.html', context)
    
    def post(self, request, *args, **kwargs):
        posts = Post.objects.all()
        form = PostForm(request.POST)
        share_form = ShareForm()

        if form.is_valid():
            newPost = form.save(commit=False)
            newPost.author = Author.objects.get(id=request.user.username)
            newPost.save()
            if newPost.type == 'post':
                newPost.source = 'http://localhost:8000/myapp/post/'+str(newPost.id)
                newPost.origin = 'http://localhost:8000/myapp/post/'+str(newPost.id)
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
        likes = Like.objects.filter(object=post)

        context = {
            'post': post,
            'form': form,
            'comments':comments,
            'likes': likes,
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
        likes = Like.objects.filter(object=post)
        likes_count = len(Like.objects.filter(object=post))

        context = {
            'post': post,
            'form': form,
            'comments':comments,
            'likes': likes,
            'likes_count': likes_count,
        }

        return render(request, 'postDetail.html', context)

class SharedPostView(View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(id=pk)
        share_form = ShareForm()

        context = {
            'post': post,
            'form': share_form,
            # 'source_post': source_post,
            # 'original_post': original_post,
        }
        return render(request, 'share.html', context)

    def post(self, request, pk, *args, **kwargs):
        source_post = Post.objects.get(pk=pk)
        original_post_id = source_post.origin.split('/')[-1]
        original_post = Post.objects.get(id=original_post_id)
        form = ShareForm(request.POST)
        
        if form.is_valid():
            new_post = Post(
            type = 'share',
            title = self.request.POST.get('title'),
            source = 'http://localhost:8000/myapp/post/'+str(pk),
            origin = original_post.origin,
            description = Post.objects.get(pk=pk).description,
            contentType = 'text',
            author = Author.objects.get(id=request.user.username),
            categories = 'categories',
            visibility = original_post.visibility, 
            )
        new_post.save()
        Inbox.objects.filter(author_id=request.user.username)[0].items.add(new_post)
        followersID = FollowerCount.objects.filter(user=request.user.username)
        for followerID in followersID:
            Inbox.objects.filter(author_id=followerID.follower)[0].items.add(new_post)
        context = {
            'new_post': new_post,
            # 'source_post': source_post,
            # 'original_post': original_post,
            'form': form,
        }
        return redirect('myapp:postList')
        #return render(request, 'share.html', context)

def like(request):
    username = request.user.username
    author = Author.objects.get(id=username)
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)
    summary = username + ' Likes your post'
    like_filter = Like.objects.filter(object=post, author=author).first()
    if like_filter == None:
        print(post, author)
        new_like = Like.objects.create(author=author, object=post)
        new_like.save()
        # like_text = 'Liked'
        post.likes += 1
        post.save()
        print("successfullt like")
        return redirect('/myapp/feed/')
    else:
        (print('successfullt unlike'))
        like_filter.delete()
        # like_text='Like'
        post.likes -= 1
        post.save()
        return redirect('/myapp/feed/')

class ShareDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(id=pk)
        
        form = CommentForm()
        comments = Comment.objects.filter(post=post).order_by('-published')
        likes = Like.objects.filter(object=post)

        source_post_id = post.source.split('/')[-1]
        source_post = Post.objects.get(id=source_post_id)
        original_post_id = post.origin.split('/')[-1]
        original_post = Post.objects.get(id=original_post_id)

        context = {
            'post': post,
            'form': form,
            'comments':comments,
            'likes': likes,
            'source_post': source_post,
            'original_post': original_post,
        }

        return render(request, 'shareDetail.html', context)
    
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
        likes = Like.objects.filter(object=post)
        likes_count = len(Like.objects.filter(object=post))

        context = {
            'post': post,
            'form': form,
            'comments':comments,
            'likes': likes,
            'likes_count': likes_count,
            # 'source_post': source_post,
            # 'original_post': original_post,

        }

        return render(request, 'shareDetail.html', context)


def liked(request, post_id):
    post = Post.objects.get(id=post_id)
    username = request.user.username
    likes_list = Like.objects.filter(object=post)
    context = {
        'likes_list': likes_list
    }
    return render(request, 'liked.html', context)
    # if 
    # like_text = 'Like'


def profile(request, user_id):
    # get basic info
    current_author_info = get_object_or_404(Author, pk=user_id)
    follower = request.user.username
    user = user_id
    # get github info
    github_username = current_author_info.github.split("/")[-1]
    # get posts
    try:
        posts = Inbox.objects.filter(author_id=user_id)[0].items
    except:
        posts = []
    # get follow
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
        'github_username': github_username,
        'posts': posts,
        }

    return render(request, 'profile.html', context)

def follow(request):
    print("follow is working")
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']
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