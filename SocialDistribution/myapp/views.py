from http.client import HTTPResponse
from urllib import request
from itertools import chain

from multiprocessing import context
from django.http import HttpResponse
from django.views import View
from .models import Post, Comment, Inbox, Like
from .forms import PostForm, CommentForm, ShareForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User, auth
from django.forms.models import model_to_dict
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import PostForm, CommentForm
from .models import Author, Post, FollowerCount, Comment, Inbox
from . import serializers
from .pagination import CustomPageNumberPagination

from ast import Delete

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView, \
    RetrieveAPIView, RetrieveDestroyAPIView
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.renderers import JSONRenderer

import re


# Create your views here.
@method_decorator(login_required, name='dispatch')
class PostListView(View):
    def get(self, request, *args, **kwargs):
        # posts = Post.objects.all().order_by('-published')
        posts = Inbox.objects.filter(author__id=request.user.username)[0].items
        author_list = Author.objects.all()
        context = {
            'postList': posts,
            'author_list':author_list,
            # 'form': form,
        }
        return render(request,'feed.html', context)

@method_decorator(login_required, name='dispatch')
class NewPostView(View):
    def get(self, request, *args, **kwargs):
        form = PostForm()
        share_form = ShareForm()
        author_list = Author.objects.all()
        context = {
            'form': form,
            'share_form': share_form,
            'author_list':author_list,
        }
        return render(request,'newpost.html', context)

    def post(self, request, *args, **kwargs):
        posts = Post.objects.all()
        share_form = ShareForm()
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            newPost = form.save(commit=False)
            newPost.author = Author.objects.get(id=request.user.username)
            newPost.save()
            if newPost.type == 'post':
                newPost.source = 'http://localhost:8000/post/'+str(newPost.id)
                newPost.origin = 'http://localhost:8000/post/'+str(newPost.id)
            newPost.save()

            Inbox.objects.filter(author__id=request.user.username)[0].items.add(newPost)
            followersID = FollowerCount.objects.filter(user=request.user.username)
            for followerID in followersID:
                Inbox.objects.filter(author__id=followerID.follower)[0].items.add(newPost)

        # posts = Post.objects.all()
        # context = {
        #     'postList': posts,
        #     # 'form': form,
        # }
        # return render(request,'myapp/newpost.html', context)
        return redirect('myapp:postList')

@method_decorator(login_required, name='dispatch')
class PostDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(id=pk)
        form = CommentForm()
        comments = Comment.objects.filter(post=post).order_by('-published')
        likes = Like.objects.filter(object=post)
        author_list = Author.objects.all()
        context = {
            'post': post,
            'form': form,
            'comments':comments,
            'likes': likes,
            'author_list':author_list,
        }

        return render(request, 'postDetail.html', context)

    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(id=pk)
        form = CommentForm(request.POST)
        author_list = Author.objects.all()
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
            'likes': likes,
            'likes_count': likes_count,
            'comments': comments,
            'author_list': author_list,
        }

        return render(request, 'postDetail.html', context)

@method_decorator(login_required, name='dispatch')
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
            source = 'http://localhost:8000/post/'+str(pk),
            origin = original_post.origin,
            description = Post.objects.get(pk=pk).description,
            contentType = 'text',
            author = Author.objects.get(id=request.user.username),
            categories = 'categories',
            visibility = original_post.visibility, 
            )
        new_post.save()
        Inbox.objects.filter(author__id=request.user.username)[0].items.add(new_post)
        followersID = FollowerCount.objects.filter(user=request.user.username)
        for followerID in followersID:
            Inbox.objects.filter(author__id=followerID.follower)[0].items.add(new_post)
        context = {
            'new_post': new_post,
            # 'source_post': source_post,
            # 'original_post': original_post,
            'form': form,
        }
        return redirect('myapp:postList')
        #return render(request, 'share.html', context)

@login_required(login_url='/accounts/login')
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
        return redirect('myapp:postList')
    else:
        (print('successfullt unlike'))
        like_filter.delete()
        # like_text='Like'
        post.likes -= 1
        post.save()
        return redirect('myapp:postList')

@method_decorator(login_required, name='dispatch')
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

@login_required(login_url='/accounts/login')
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

@login_required(login_url='/accounts/login')
def profile(request, user_id):
    # get basic info
    current_author_info = get_object_or_404(Author, pk=user_id)
    follower = request.user.username
    user = user_id
    # get github info
    github_username = current_author_info.github.split("/")[-1]
    # get posts
    try:
        posts = Post.objects.filter(author__id=user_id).order_by('-published')
    except:
        posts = []
    # get follow
    if FollowerCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'
    count_followers = len(FollowerCount.objects.filter(user=user_id))
    count_following = len(FollowerCount.objects.filter(follower=user_id))
    author_list = Author.objects.all()
    context = {
        'current_author_info': current_author_info,
        'button_text': button_text,
        'count_followers': count_followers,
        'count_following': count_following,
        'github_username': github_username,
        'posts': posts,
        'author_list': author_list,
        }

    return render(request, 'profile.html', context)

@login_required(login_url='/accounts/login')
def follow(request):
    print("follow is working")
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']
        if FollowerCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowerCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('myapp:profile', user_id=user)
        else:
            new_follower = FollowerCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('myapp:profile', user_id=user)
    else:
        return redirect('/')

@login_required(login_url='/accounts/login')
def search(request):
    author_list = Author.objects.all()
    return render(request, 'feed.html', {'author_list':author_list})

@login_required(login_url='/accounts/login')
def getuser(request):
    username = request.GET['username']
    try:
        current_author_info = Author.objects.get(displayName = username)
    except:
        current_author_info = None
    if current_author_info == None:
        author_list = Author.objects.all()
        context = {
            'username':username,
            'author_list':author_list,
        }
        return render(request, 'profileNotFound.html', context)
    # current_author_info = get_object_or_404(Author, displayName = username)
    else:
        user_id = current_author_info.id
        return redirect('myapp:profile', user_id=user_id)

@method_decorator(login_required, name='dispatch')
class PostEditView(UpdateView):
    model = Post
    fields = ['title','description','visibility']
    template_name = 'postEdit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('myapp:postDetail', kwargs={'pk':pk})

@method_decorator(login_required, name='dispatch')
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'postDelete.html'
    success_url = reverse_lazy('myapp:postList')

# API

# class authorsAPI(APIView):
#
#     # pagination_class = CustomPageNumberPagination
#
#     def get(self, request):
#         author1 = Author.objects.all()
#         serializer = AuthorSerializer(author1, many=True)
#         return Response(serializer.data)

class AuthorAPIView(RetrieveUpdateAPIView):
    """ GET or PUT an Author object """
    # note that PUT is updating an author object

    serializer_class = serializers.AuthorSerializer
    lookup_field = "id"

    def get_queryset(self):
        username = self.kwargs['id']
        return Author.objects.filter(id=username)

class AuthorsAPIView(ListAPIView):
    """ GET Authors (with pagination support)"""

    # resource https://www.youtube.com/watch?v=eaWzTMtrcrE&list=PLx-q4INfd95FWHy9M3Gt6NkUGR2R2yqT8&index=9
    serializer_class = serializers.AuthorSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return Author.objects.all()


class FollowersAPIView(RetrieveAPIView):
    """ GET an Author's all followers """

    # serializer_class = serializers.FollowersSerializer

    def retrieve(self, request, *args, **kwargs):
        queryset = []
        username = self.kwargs['author']
        followers = FollowerCount.objects.filter(user=username)
        for follower in followers:
            author = model_to_dict(Author.objects.filter(id=follower.follower).first())
            queryset.append(author)
        return Response(queryset)




class FollowerAPIView(RetrieveUpdateDestroyAPIView):
    """ GET if is a follower PUT a new follower DELETE an existing follower"""

    serializer_class = serializers.FollowersSerializer
    renderer_classes = [JSONRenderer]


    def relation_check(self, *args, **kwargs):
        username = self.kwargs['author']
        another = self.kwargs['another_author']
        followers = FollowerCount.objects.filter(user=username).values_list('follower', flat=True)
        if another in followers:
            return True
        return False


    def retrieve(self, request, *args, **kwargs):

        if self.relation_check():
            return Response({'following_relation_exist': 'True'})
        else:
            return Response({'following_relation_exist': 'False'})

    def put(self, request, *args, **kwargs):
        if self.relation_check():
            return Response({'following_relation_exist': 'True',
                             'following_relation_add': 'False'})
        else:
            try:
                FollowerCount.objects.create(follower=self.kwargs['another_author'], user=self.kwargs['author'])
                return Response({'following_relation_exist': 'False',
                                 'following_relation_put': 'True'})
            except:
                return Response({'following_relation_exist': 'False',
                                 'following_relation_put': 'False'})

    def delete(self, request, *args, **kwargs):
        if self.relation_check():
            relation = FollowerCount.objects.filter(follower=self.kwargs['another_author']).filter(user=self.kwargs['author'])
            try:
                relation.delete()
                return Response({'following_relation_exist': 'True',
                                 'following_relation_delete': 'True'})
            except:
                return Response({'following_relation_exist': 'True',
                                 'following_relation_delete': 'False'})
        else:
            return Response({'following_relation_exist': 'False',
                                 'following_relation_delete': 'False'})

# TODO FollowRequest is not complete

class PostAPIView(CreateModelMixin, RetrieveUpdateDestroyAPIView):
    """ GET POST PUT DELETE a post"""
    # note that POST is creating a new post
    # note that PUT is updating an existing post

    serializer_class = serializers.PostSerializer
    lookup_fields = ('pk', 'author')

    def get_queryset(self):
        username = self.kwargs['author']
        post_id = self.kwargs['pk']
        return Post.objects.filter(id=post_id, author=username)

    def post(self, request, *args, **kwargs):
        # TODO Push the post into the inbox
        return self.create(request, *args, **kwargs)

class PostsAPIView(ListCreateAPIView):
    """ GET all posts or POST a new post (with pagination support) """

    serializer_class = serializers.PostSerializer
    pagination_class = CustomPageNumberPagination
    lookup_field = 'author'

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        username = self.kwargs['author']
        return Post.objects.filter(author=username)

# TODO ImagePost API is not complete

# TODO write this when author is linked in
# class CommentsAPIView(ListCreateAPIView):
#     """ GET all comments or POST a new comment (with pagination support) """
#
#     serializer_class = serializers.CommentSerializer
#     pagination_class = CustomPageNumberPagination
#     lookup_fields = ('post', 'author')
#
#     def get_queryset(self):
#         username = self.kwargs['author']
#         post_id = self.kwargs['post']
#         return Post.objects.filter(author=username, post=post_id)

# TODO Like API

# TODO Liked API

# TODO Inbox API can start on Mar.2 (after meeting)