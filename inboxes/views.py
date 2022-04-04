import requests
from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
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
from posts.models import Post, Category, Like, Comment
from . import serializers
from .models import Inbox, InboxItem
from common.views import localHostList

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
            post_obj = post.item
            # display only if it is not unlisted
            if not post_obj.unlisted:
                post_obj.uuid = post_obj.id.split('/')[-1]
                responsePosts.append(post_obj)

        # sort responsePosts by published
        responsePosts.sort(key=lambda x: x.published, reverse=True)

        # make get request to other nodes, to get remote authors
        # TODO: This is going to change once the other groups implement pagination
        for node in connectionNodes:
            print(node, '-', node.url)
            if 'project-socialdistribution.herokuapp.com' in node.url:
                '''adapter for team Ma'''
                tempNodeURL = 'https://project-socialdistribution.herokuapp.com/'
                response = requests.get(f"{tempNodeURL}authors/",
                                    params=request.GET,
                                    auth=HTTPBasicAuth(node.auth_username,
                                                       node.auth_password))
                if response.status_code == 200:
                    authors = response.json()['items']
                    for author in authors:
                        if 'project-socialdistribution.herokuapp.com' not in author['host']:
                            continue
                        authorID = author['id']
                        tempAuthorID = authorID[:4]+'s'+authorID[4:]
                        if not (Author.objects.filter(id=tempAuthorID).exists()):
                            print(tempAuthorID.split('/'))
                            Author.objects.create(
                                id=tempAuthorID,
                                # username = remote_author.uuid
                                username=tempAuthorID.split('/')[-2],
                                displayName=author['displayName'],
                                profileImage=author['profileImage'],
                                github=author['github'],
                                host=author['host'],
                                url=author['url'])
            else:
                response = requests.get(f"{node.url}authors/",
                                    params=request.GET,
                                    auth=HTTPBasicAuth(node.auth_username,
                                                       node.auth_password))
                # breakpoint()
                if response.status_code == 200:
                    authors = response.json()['items']
                    for author in authors:
                        try:
                            if not (Author.objects.filter(id=author['id']).exists()):
                                Author.objects.create(
                                    id=author['id'],
                                    # username = remote_author.uuid
                                    username=author['id'].split('/')[-1],
                                    displayName=author['displayName'],
                                    profileImage=author['profileImage'],
                                    github=author['github'],
                                    host=author['host'],
                                    url=author['url'])
                        except Exception as e:
                            print(f"error occurs: {e}, maybe missing")
                else:
                    print(response)

        author_list = Author.objects.all()
        context = {
            'postList': responsePosts,
            'author_list': author_list,
        }
        return render(request, 'feed.html', context)

@method_decorator(login_required, name='dispatch')
class OneToOneView(View):
    def get(self, request, *args, **kwargs):
        # posts = Post.objects.all().order_by('-published')
        currentUser = request.user
        currentInbox = Inbox.objects.filter(
            author__username=currentUser.username).first()
        posts = currentInbox.inboxitem_set.filter(inbox_item_type="post")
        responsePosts = []
        for post in posts:
            post_obj = post.item
            post_obj.uuid = post_obj.id.split('/')[-1]
            responsePosts.append(post_obj)
        # sort responsePosts by published
        responsePosts.sort(key=lambda x: x.published, reverse=True)

        author_list = Author.objects.all()
        context = {
            'postList': responsePosts,
            'author_list':author_list,

            # 'form': form,
        }
        return render(request,'1to1.html', context)


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
            return HttpResponseNotFound("author (in url) does not exist")
        data = request.data

        # try:
        # 1. publish a post
        # don't care if these two have a friend relation,
        # just push the post into its follower's inbox
        if data["type"].lower() == "post":
            # check if user in the body (who post the post) exists
            author = Author.objects.filter(id=data["author"]["id"]).first()
            if author is None:
                return HttpResponseNotFound("author (in body) not exist")
            if data['published']:
                new_post = Post.objects.create(
                    title=data["title"],
                    description=data["description"],
                    content=data["content"],
                    contentType=data["contentType"],
                    author=author,
                    unparsedCategories=data["categories"],
                    visibility=data["visibility"],
                    image_b64=data["image_b64"],
                    id=data['id'],
                    source=data['source'],
                    origin=data['origin'],
                    comments=data['comments'],
                    published=data['published']
                )
            else:
                # creating new post
                new_post = Post.objects.create(
                    title=data["title"],
                    description=data["description"],
                    content=data["content"],
                    contentType=data["contentType"],
                    author=author,
                    unparsedCategories=data["categories"],
                    visibility=data["visibility"],
                    image_b64=data["image_b64"],
                    id=data['id'],
                    source=data['source'],
                    origin=data['origin'],
                    comments=data['comments']
                )

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

            # adding post to author inbox via InboxItem
            InboxItem.objects.create(
                inbox=Inbox.objects.filter(
                    author__username=current_user.username).first(),
                item=new_post,
                inbox_item_type="post",
            )

            serializer = serializers.PostSerializer(new_post)
            return Response(serializer.data)

        # 2. adding follow to user inbox
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

            # add friendfollowrequest to the inbox as well
            InboxItem.objects.create(
                inbox=Inbox.objects.filter(
                    author__username=current_user.username).first(),
                item=friend_request,
                inbox_item_type="follow",
            )

            serializer = serializers.FriendFollowRequestSerializer(
                friend_request)
            return Response(serializer.data)

        elif data["type"].lower() == "like":
            # check if this is a comment or a post
            if "comment" in data["object"]:
                # check if the comment exists
                comment = Comment.objects.filter(id=data["object"]).first()
                if comment is None:
                    return HttpResponseNotFound("comment not exist")
                like_before = Like.objects.filter(author__id=data['author']['id'],
                                                  object=comment.id).first()
                if like_before is not None:
                    return HttpResponseNotFound("user has given a like before")
            else:
                # like a post
                # check if post (the post that user gives a like) exists
                post = Post.objects.filter(id=data["object"]).first()
                # people only send like object on posts that is originated from our node, so a checking is a must
                if post is None:
                    return HttpResponseNotFound("post not exist")
                like_before = Like.objects.filter(author__id=data['author']['id'],
                                                  object=post.id).first()
                if like_before is not None:
                    return HttpResponseNotFound("user has given a like before")

                post.likes += 1
                post.save()

            author = Author.objects.filter(id=data['author']['id']).first()
            try:
                new_like = Like.objects.create(author=author, object=data["object"], summary=data['summary'])
                new_like.save()
            except Exception as e:
                return HttpResponseNotFound(f"there was a problem when processing {e}")

            if data['type'] == "post":
                post.likes += 1
                post.save()

            # adding like to user inbox via InboxItem
            InboxItem.objects.create(
                inbox=Inbox.objects.filter(
                    author__username=current_user.username).first(),
                item=new_like,
                inbox_item_type="like",
            )
            serializer = serializers.LikesSerializer(new_like)
            return Response(serializer.data)

        elif data["type"].lower() == "comment":
            split_contents = data['id'].split('/')
            # post id
            post_id = split_contents[split_contents.index('posts') + 1]
            # comment id
            comment_id = split_contents[split_contents.index('comments') + 1]
            
            # check if post exists in db
            if not Post.objects.filter(id__contains=post_id).first():
                return HttpResponseNotFound("post does not exist")

            # # check if the comment already exists in db for specific post
            # if Post.objects.filter(id__contains=post_id):
            #     return HttpResponseNotFound("comment on post already exists")
            # creating comment object
            try:
                # must create author first
                new_author = Author.objects.get(id=data['author']['id'])
                new_comment = Comment.objects.create(author=new_author, comment=data['comment'], contentType=data['contentType'], id=data['id'])
                new_comment.save()
            except Exception as e:
                return HttpResponseNotFound(f"there was a problem when processing {e}")

            # adding comment to post object
            post = Post.objects.filter(id__contains=post_id).first()
            post.count += 1   
            post.save()

            # adding comment to user inbox via InboxItem
            InboxItem.objects.create(
                inbox=Inbox.objects.filter(
                    author__username=current_user.username).first(),
                item=new_comment,
                inbox_item_type="comment",
            )

            serializer = serializers.CommentsSerializer(new_comment)
            return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        author_uuid = self.kwargs['author']
        author = Author.objects.filter(uuid=author_uuid).first()
        inbox = Inbox.objects.filter(author=author.username).first()
        inbox.delete()
        new_inbox = Inbox.objects.create(author=author)
        new_inbox.save()

        serializer = serializers.InboxSerializer(new_inbox)
        return Response(serializer.data)
