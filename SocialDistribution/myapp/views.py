from http.client import HTTPResponse
from itertools import chain

from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User, auth
from django.forms.models import model_to_dict
from rest_framework.renderers import JSONRenderer

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
import re

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