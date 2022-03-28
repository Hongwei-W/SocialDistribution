import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from requests.auth import HTTPBasicAuth
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response

from authors.models import Author, FriendFollowRequest
from common.models import ConnectionNode
from common.pagination import CustomPageNumberPagination
from posts.models import Post, Category, Like
from . import serializers
from .models import Inbox

localHostList = [
    'http://127.0.0.1:7070/', 'http://127.0.0.1:8000/',
    'http://localhost:8000', 'http://localhost:8000/',
    'https://c404-social-distribution.herokuapp.com/'
]

connectionNodes = ConnectionNode.objects.all()


# Create your views here.
@method_decorator(login_required, name='dispatch')
class PostListView(View):

    def get(self, request, *args, **kwargs):
        # getting all posts object from inbox
        currentUser = request.user
        currentInbox = Inbox.objects.filter(
            author__username=currentUser.username).first()
        posts = currentInbox.inboxitem_set.filter(inbox_item_type="post")
        responsePosts = []
        for post in posts:
            responsePosts.append(post.item)
        # sort responsePosts by published
        responsePosts.sort(key=lambda x: x.published, reverse=True)

        for node in connectionNodes:
            # make get request to other nodes
            response = requests.get(f"{node.url}authors/",
                                    params=request.GET,
                                    auth=HTTPBasicAuth(node.auth_username,
                                                       node.auth_password))
            if response.status_code == 200:
                authors = response.json()['items']
                for author in authors:
                    if not (Author.objects.filter(id=author['id']).exists()):
                        Author.objects.create(
                            id=author['id'],
                            # username = remote_author.uuid
                            username=author['id'].split('/')[-1],
                            displayName=author['displayName'],
                            profileImage=author['profileImage'],
                            github=author['github'],
                            host=author['host'])
            else:
                print(response)

        author_list = Author.objects.all()
        context = {
            'postList': responsePosts,
            'author_list': author_list,
            # 'form': form,
        }
        return render(request, 'feed.html', context)

#
# API
#

class InboxAPIView(CreateModelMixin, RetrieveDestroyAPIView):
    """ GET inbox POST post/follow/like DELETE inbox_obj"""
    serializer_class = serializers.InboxSerializer
    pagination_class = CustomPageNumberPagination
    lookup_fields = ('author', )

    def get_object(self):
        author_uuid = self.kwargs['author']
        author = Author.objects.filter(uuid=author_uuid).first()
        return Inbox.objects.filter(author__username=author.username).first()

    def post(self, request, *args, **kwargs):
        # check if user in url exists
        uuid = self.kwargs['author']
        current_user = Author.objects.filter(uuid=uuid).first()
        if current_user is None:
            return HttpResponseNotFound("author (in url) not exist")
        data = request.data

        # try:
        # 1. publish a post
        # don't care if these two have a friend relation, just push the post into its follower's inbox
        if data["type"] == "post":
            # check if user in the body (who post the post) exists
            author = Author.objects.filter(id=data["author"]["id"]).first()
            if author is None:
                return HttpResponseNotFound("author (in body) not exist")

            new_post = Post.objects.create(
                title=data["title"],
                description=data["description"],
                content=data["content"],
                contentType=data["contentType"],
                author=author,
                unparsedCategories=data["categories"],
                visibility=data["visibility"],
                image_b64=data["image_b64"])
            unparsed_cat = new_post.unparsedCategories
            for cat in unparsed_cat:
                new_cat = Category()
                new_cat.cat = cat
                new_cat.save()
                new_post.categories.add(new_cat)
                new_post.save()

            try:
                new_post.save()
            except Exception as e:
                return HttpResponseNotFound(e)
            new_post.id = request.get_host() + "/authors/" + str(
                new_post.author.uuid) + "/posts/" + str(new_post.uuid)
            new_post.source = request.get_host() + "/post/" + str(
                new_post.uuid)
            new_post.origin = request.get_host() + "/post/" + str(
                new_post.uuid)
            new_post.comments = request.get_host() + "/post/" + str(
                new_post.uuid)
            new_post.save()
            Inbox.objects.filter(
                author__username=current_user.username)[0].items.add(new_post)

            serializer = serializers.PostSerializer(new_post)
            return Response(serializer.data)

        elif data["type"].lower() == "follow":
            remote_author = Author.objects.filter(
                id=data['actor']['id']).first()
            our_author = Author.objects.filter(
                username=data['object']['displayName']).first()
            friend_request = FriendFollowRequest.objects.create(
                summary=data["summary"],
                actor=remote_author,
                object=our_author)
            friend_request.save()

            serializer = serializers.FriendFollowRequestSerializer(
                friend_request)
            return Response(serializer.data)

        elif data["type"] == "like":
            # check if post in the body (the post that user gives a like) exists
            post = Post.objects.filter(uuid=data["object"]).first()
            if post is None:
                return HttpResponseNotFound("post not exist")
            like_before = Like.objects.filter(author=current_user,
                                              object=post).first()
            if like_before is not None:
                return HttpResponseNotFound("user has given a like before")
            new_like = Like.objects.create(author=current_user, object=post)
            new_like.save()
            post.likes += 1
            post.save()
            # TODO like could be comments/posts
            serializer = serializers.LikeSerializer(new_like)
            # TODO push into inbox
            return Response(serializer.data)

        # except Exception as e:
        #     return HttpResponseNotFound(e)

    def delete(self, request, *args, **kwargs):
        author_uuid = self.kwargs['author']
        author = Author.objects.filter(uuid=author_uuid).first()
        inbox = Inbox.objects.filter(author=author.username).first()
        inbox.delete()
        new_inbox = Inbox.objects.create(author=author)
        new_inbox.save()

        serializer = serializers.InboxSerializer(new_inbox)
        return Response(serializer.data)
