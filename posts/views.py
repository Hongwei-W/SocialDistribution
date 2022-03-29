import base64
import json

import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.edit import UpdateView, DeleteView
from requests.auth import HTTPBasicAuth
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, \
    RetrieveAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response

from authors.models import Author, Followers, FollowerCount
from common.models import ConnectionNode
from common.pagination import CustomPageNumberPagination
from inboxes.models import Inbox, InboxItem
from . import serializers, renderers
from .forms import PostForm, CommentForm, ShareForm
from .models import Post, Comment, Category, Like

localHostList = [
    'http://127.0.0.1:7070/', 'http://127.0.0.1:8000/',
    'http://localhost:8000', 'http://localhost:8000/',
    'https://c404-social-distribution.herokuapp.com/'
]

connectionNodes = ConnectionNode.objects.all()

@method_decorator(login_required, name='dispatch')
class NewPostView(View):

    def get(self, request, *args, **kwargs):
        form = PostForm()
        share_form = ShareForm()
        author_list = Author.objects.all()
        context = {
            'form': form,
            'share_form': share_form,
            'author_list': author_list,
        }
        return render(request, 'newpost.html', context)

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            # creating post from form and adding attributes
            newPost = form.save(commit=False)
            newPost.author = Author.objects.get(username=request.user.username)
            newPost.id = request.get_host() + "/authors/" + str(
                newPost.author.uuid) + "/posts/" + str(newPost.uuid)

            # adding categories to post
            unparsedCat = newPost.unparsedCategories
            catList = unparsedCat.split()
            newPost.save()
            for cat in catList:
                newCat = Category()
                newCat.cat = cat
                newCat.save()
                newPost.categories.add(newCat)
                newPost.save()

            # not sure what its for but it works
            if newPost.type == 'post':
                newPost.source = request.get_host() + "/post/" + str(
                    newPost.uuid)
                newPost.origin = request.get_host() + "/post/" + str(
                    newPost.uuid)
                newPost.comments = request.get_host() + "/post/" + str(
                    newPost.uuid) + '/comments'
                newPost.save()

            # if its an image
            if newPost.post_image:
                # print("------url", newPost.post_image.path)
                # print(str(newPost.post_image))
                img_file = open(newPost.post_image.path, "rb")
                newPost.image_b64 = base64.b64encode(img_file.read())
                # print(newPost.image_b64[:20])
                newPost.save()

            # add post to InboxItem which links to Inbox
            InboxItem.objects.create(
                inbox=Inbox.objects.filter(
                    author__username=request.user.username).first(),
                inbox_item_type="post",
                item=newPost,
            )

            user = Author.objects.get(username=request.user.username)
            try:
                followersID = Followers.objects.filter(
                    user__username=user.username).first().items.all()
                for follower in followersID:
                    # follower is <author> object
                    # if follower is local
                    if follower.host in localHostList:
                        # add it to inbox of follower
                        InboxItem.objects.create(
                            inbox=Inbox.objects.filter(
                                author__username=follower.username).first(),
                            inbox_item_type="post",
                            item=newPost,
                        )
                    else:
                        # if author is not local make post request to add to other user inbox
                        serializer = serializers.PostSerializer(newPost)

                        # get follower node object
                        followerNode = connectionNodes.filter(
                            url=f"{follower.host}service/").first()
                        req = requests.Request(
                            'POST',
                            f"{followerNode.url}authors/{follower.username}/inbox",
                            data=json.dumps(serializer.data),
                            auth=HTTPBasicAuth(followerNode.auth_username,
                                               followerNode.auth_password),
                            headers={'Content-Type': 'application/json'})

                        prepared = req.prepare()

                        s = requests.Session()
                        resp = s.send(prepared)

                        print("status code, ", resp.status_code)

            except AttributeError as e:
                print(e, 'No followers for this author')

        return redirect('inboxes:postList')


@method_decorator(login_required, name='dispatch')
class PostDetailView(View):

    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(uuid=pk)
        form = CommentForm()
        comments = Comment.objects.filter(post=post).order_by('-published')
        likes = Like.objects.filter(object=post)
        author_list = Author.objects.all()
        if post.post_image:
            image_b64 = post.image_b64.decode('utf-8')
        else:
            image_b64 = ''
        context = {
            'post': post,
            'form': form,
            'comments': comments,
            'likes': likes,
            'author_list': author_list,
            'image_b64': image_b64,
        }

        return render(request, 'postDetail.html', context)

    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(uuid=pk)
        form = CommentForm(request.POST)
        author_list = Author.objects.all()
        if form.is_valid():
            newComment = form.save(commit=False)
            newComment.author = Author.objects.get(
                username=request.user.username)
            newComment.post = post
            newComment.save()
            newComment.id = request.get_host() + "/authors/" + str(
                post.author.uuid) + "/posts/" + str(pk) + "/comments/" + str(
                    newComment.uuid)
            newComment.save()
            post.count += 1
            post.save()
            # reset form
            form = CommentForm()

        comments = Comment.objects.filter(post=post).order_by('-published')
        likes = Like.objects.filter(object=post)
        likes_count = len(Like.objects.filter(object=post))
        if post.image_b64 != None:
            image_b64 = post.image_b64.decode('utf-8')
            context = {
                'post': post,
                'form': form,
                'likes': likes,
                'likes_count': likes_count,
                'comments': comments,
                'author_list': author_list,
                'image_b64': image_b64,
            }
        else:
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
    """
        View for sharing posted posts (or something like that)
    """

    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(uuid=pk)
        share_form = ShareForm()

        context = {
            'post': post,
            'form': share_form,
            # 'source_post': source_post,
            # 'original_post': original_post,
        }
        return render(request, 'share.html', context)

    def post(self, request, pk, *args, **kwargs):
        # source_post is the currently selected post to be shared
        source_post = Post.objects.get(pk=pk)
        # TODO: SU: please confirm that this is accepted behaviour.
        if source_post.type == 'post':
            source_text = request.get_host() + '/post/'
        else:
            source_text = request.get_host() + '/post/shared/'
        original_post_id = source_post.origin.split('/')[-1]
        original_post = Post.objects.get(uuid=original_post_id)
        form = ShareForm(request.POST)

        if form.is_valid():
            new_post = Post(
                #TODO: Su: please confirm that type is allowed to be updated
                # eg if author.user is not the same as the user who is sharing the post
                type='share',
                title=self.request.POST.get('title'),
                source=source_text + str(pk),
                origin=original_post.origin,
                description=Post.objects.get(pk=pk).description,
                content=Post.objects.get(pk=pk).content,
                contentType='text',
                author=Author.objects.get(username=request.user.username),
                visibility=original_post.visibility,
            )
            new_post.save()
            new_post.id = request.get_host() + "/authors/" + str(
                new_post.author.uuid) + "/posts/" + str(new_post.uuid)
            new_post.save()

        # adding post to request.user's inbox
        InboxItem.objects.create(
            inbox=Inbox.objects.filter(
                author__username=request.user.username).first(),
            inbox_item_type='post',
            item=new_post,
        )

        try:
            followers = Followers.objects.get(
                user__username=request.user.username).items.all()
            # followersID = FollowerCount.objects.filter(user=request.user.username)
            for follower in followers:
                # follower is <author> object
                InboxItem.objects.create(
                    inbox=Inbox.objects.filter(
                        author__username=follower.username).first(),
                    inbox_item_type='post',
                    item=new_post,
                )
                # TODO: darren make this work for remote authors too (just call API or something lol)
        except Exception as e:
            print(e, 'No followers for this author')

        context = {
            'new_post': new_post,
            # 'source_post': source_post,
            # 'original_post': original_post,
            'form': form,
        }
        return redirect('inboxes:postList')


@login_required(login_url='/accounts/login')
def like(request):
    username = request.user.username
    author = Author.objects.get(username=username)
    post_id = request.GET.get('post_id')
    post = Post.objects.get(uuid=post_id)
    summary = username + ' Likes your post'
    like_filter = Like.objects.filter(object=post, author=author).first()
    if like_filter == None:
        print(post, author)
        new_like = Like.objects.create(author=author, object=post)
        new_like.save()
        post.likes += 1
        post.save()

        # push like object into inbox
        InboxItem.objects.create(
            inbox=Inbox.objects.filter(
                author__username=post.author.username).first(),
            inbox_item_type='like',
            item=new_like,
        )

        # return redirect('inboxes:postList')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        like_filter.delete()
        # also delete InboxItem for that like (will never be none)
        InboxItem.objects.filter(
            inbox_item_type='like', item=like_filter).delete()
        # like_text='Like'
        post.likes -= 1
        post.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@method_decorator(login_required, name='dispatch')
class ShareDetailView(View):

    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(uuid=pk)

        form = CommentForm()
        comments = Comment.objects.filter(post=post).order_by('-published')
        likes = Like.objects.filter(object=post)

        source_post_id = post.source.split('/')[-1]
        source_post = Post.objects.get(uuid=source_post_id)
        original_post_id = post.origin.split('/')[-1]
        original_post = Post.objects.get(uuid=original_post_id)

        context = {
            'post': post,
            'form': form,
            'comments': comments,
            'likes': likes,
            'source_post': source_post,
            'original_post': original_post,
        }

        return render(request, 'shareDetail.html', context)

    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(uuid=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            newComment = form.save(commit=False)
            newComment.author = Author.objects.get(
                username=request.user.username)
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
            'comments': comments,
            'likes': likes,
            'likes_count': likes_count,
            # 'source_post': source_post,
            # 'original_post': original_post,
        }

        return render(request, 'shareDetail.html', context)


@login_required(login_url='/accounts/login')
def liked(request, post_id):
    post = Post.objects.get(uuid=post_id)
    username = request.user.username
    likes_list = Like.objects.filter(object=post)
    context = {'likes_list': likes_list}
    return render(request, 'liked.html', context)
    # if
    # like_text = 'Like'


@method_decorator(login_required, name='dispatch')
class PostEditView(UpdateView):
    model = Post
    fields = ['title', 'content', 'contentType', 'visibility']
    template_name = 'postEdit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('posts:postDetail', kwargs={'pk': pk})


@method_decorator(login_required, name='dispatch')
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'postDelete.html'
    success_url = reverse_lazy('posts:postList')


#
# API
#


class PostAPIView(CreateModelMixin, RetrieveUpdateDestroyAPIView):
    """ GET POST PUT DELETE a post"""
    # note that POST is creating a new post
    # note that PUT is updating an existing post
    # TODO rewrite the PUT method

    serializer_class = serializers.PostSerializer
    # renderer_classes = (renderers.PostRenderer, )
    lookup_fields = ('pk', 'author')

    def get_queryset(self):
        author_uuid = self.kwargs['author']
        author = Author.objects.filter(uuid=author_uuid).first()
        post_id = self.kwargs['pk']
        return Post.objects.filter(uuid=post_id, author=author.username)

    def post(self, request, *args, **kwargs):
        author_uuid = self.kwargs['author']
        post_id = self.kwargs['pk']
        author = Author.objects.filter(uuid=author_uuid).first()
        if author is None:
            return HttpResponseNotFound("author not exist")
        data = request.data
        try:
            new_post = Post.objects.create(
                title=data["title"],
                uuid=post_id,
                description=data["description"],
                content=data["content"],
                contentType=data["contentType"],
                author=author,
                unparsedCategories=data["categories"],
                visibility=data["visibility"],
                image_b64=data["post_image"])
            unparsed_cat = new_post.unparsedCategories
            cat_list = unparsed_cat.split()
            for cat in cat_list:
                new_cat = Category()
                new_cat.cat = cat
                new_cat.save()
                new_post.categories.add(new_cat)
                new_post.save()

            new_post.id = request.get_host() + "/authors/" + str(
                new_post.author.uuid) + "/posts/" + str(new_post.uuid)
            new_post.source = request.get_host() + "/post/" + str(
                new_post.uuid)
            new_post.origin = request.get_host() + "/post/" + str(
                new_post.uuid)
            new_post.comments = request.get_host() + "/post/" + str(
                new_post.uuid) + '/comments'
            new_post.save()
        except Exception as e:
            return HttpResponseNotFound(e)

        # TODO: lucas charles: verify this part doesnt need image post stuff like on
        # line 163 of this file.\

        # adding post to inbox of current author
        # add post to InboxItem which links to Inbox
        InboxItem.objects.create(
            inbox=Inbox.objects.filter(
                author__username=author.username).first(),
            inbox_item_type='post',
            item=new_post,
        )

        # adding post to inbox of all followers of current author
        followers = Followers.objects.filter(user=author.username)
        for follower in followers:
            InboxItem.objects.create(
                inbox=Inbox.objects.filter(
                    author__username=follower.username).first(),
                inbox_item_type='post',
                item=new_post,
            )
        serializer = serializers.PostSerializer(new_post)
        return Response(serializer.data)


class PostsAPIView(CreateModelMixin, ListAPIView):
    """ GET all posts or POST a new post (with pagination support) """

    serializer_class = serializers.PostSerializer
    pagination_class = CustomPageNumberPagination
    # renderer_classes = (renderers.PostsRenderer, )
    lookup_field = 'author'

    def post(self, request, *args, **kwargs):
        author_uuid = self.kwargs['author']
        author = Author.objects.filter(uuid=author_uuid).first()
        if author is None:
            return HttpResponseNotFound("author not exist")
        data = request.data
        try:
            new_post = Post.objects.create(
                title=data["title"],
                description=data["description"],
                content=data["content"],
                contentType=data["contentType"],
                author=author,
                unparsedCategories=data["categories"],
                visibility=data["visibility"],
                post_image=data["post_image"])
            unparsed_cat = new_post.unparsedCategories
            cat_list = unparsed_cat.split()
            for cat in cat_list:
                new_cat = Category()
                new_cat.cat = cat
                new_cat.save()
                new_post.categories.add(new_cat)
                new_post.save()

            new_post.save()
        except Exception as e:
            return HttpResponseNotFound(e)
        new_post.id = request.get_host() + "/authors/" + str(
            new_post.author.uuid) + "/posts/" + str(new_post.uuid)
        new_post.source = request.get_host() + "/post/" + str(new_post.uuid)
        new_post.origin = request.get_host() + "/post/" + str(new_post.uuid)
        new_post.comments = request.get_host() + "/post/" + str(new_post.uuid)
        new_post.save()

        # adding post to inbox of current author
        # add post to InboxItem which links to Inbox
        InboxItem.objects.create(
            inbox=Inbox.objects.filter(
                author__username=author.username).first(),
            inbox_item_type='post',
            item=new_post,
        )

        # adding post to inbox of all followers of current author
        followers = Followers.objects.filter(user=author.username)
        for follower in followers:
            InboxItem.objects.create(
                inbox=Inbox.objects.filter(
                    author__username=follower.username).first(),
                inbox_item_type='post',
                item=new_post,
            )

        serializer = serializers.PostSerializer(new_post)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        author_uuid = self.kwargs['author']
        author = Author.objects.filter(uuid=author_uuid).first()
        posts = Post.objects.filter(author__username=author.username,
                                    visibility="PUBLIC")
        serializer = serializers.PostSerializer(posts, many=True)
        return Response({"type": "posts", "items": serializer.data})


class ImagePostAPIView(RetrieveAPIView):
    """ GET an image post"""

    serializer_class = serializers.PostSerializer
    renderer_classes = (renderers.ImagePostRenderer, )
    lookup_fields = ('uuid', 'author')

    def get_queryset(self):
        author_uuid = self.kwargs['author']
        author = Author.objects.filter(uuid=author_uuid).first()
        post_id = self.kwargs['pk']
        return Post.objects.filter(uuid=post_id, author=author.username)


class CommentsAPIView(CreateModelMixin, ListAPIView):
    """ GET all comments or POST a new comment (with pagination support) """
    # TODO pagination failed
    serializer_class = serializers.CommentsSerializer
    pagination_class = CustomPageNumberPagination
    # renderer_classes = (renderers.CommentsRenderer, )
    lookup_fields = ('post', )

    def list(self, request, *args, **kwargs):
        post_id = self.kwargs['post']
        serializer = serializers.CommentsSerializer(
            Comment.objects.filter(post=post_id), many=True)
        return Response({"type": "comments", "items": serializer.data})

    def post(self, request, *args, **kwargs):
        current_user_uuid = self.kwargs['author']
        current_user = Author.objects.filter(uuid=current_user_uuid).first()
        post_id = self.kwargs['post']
        post = Post.objects.filter(uuid=post_id).first()
        if current_user is None or post is None:
            return HttpResponseNotFound("author or post not exist")

        data = request.data
        new_comment = Comment.objects.create(author=current_user,
                                             comment=data["comment"],
                                             contentType=data["contentType"],
                                             post=post)
        new_comment.save()
        new_comment.id = request.get_host() + "/authors/" + str(
            post.author.uuid) + "/posts/" + str(
                post.uuid) + "/comments/" + str(new_comment.uuid)
        new_comment.save()
        post.count += 1
        post.save()
        serializer = serializers.CommentsSerializer(new_comment)
        return Response(serializer.data)


# TODO Like API - 1: send a like object


class LikesAPIView(ListAPIView):
    serializer_class = serializers.LikesSerializer
    pagination_class = CustomPageNumberPagination
    # renderer_classes = (renderers.LikesRenderer,)
    lookup_fields = ('object', )

    def get_queryset(self):
        post_id = self.kwargs['post']
        return Like.objects.filter(object=post_id)


# TODO Like API - 3: comment likes


class LikedAPIView(ListAPIView):
    serializer_class = serializers.LikesSerializer
    pagination_class = CustomPageNumberPagination
    # renderer_classes = (renderers.LikedRenderer,)
    lookup_fields = ('author', )

    def list(self, request, *args, **kwargs):
        author_uuid = self.kwargs['author']
        author = Author.objects.filter(uuid=author_uuid).first()
        like = Like.objects.filter(object__visibility="PUBLIC",
                                   author=author.username)
        serializer = serializers.LikesSerializer(like, many=True)
        return Response({"type": "liked", "items": serializer.data})
