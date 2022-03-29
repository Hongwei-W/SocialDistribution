import json

import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from requests.auth import HTTPBasicAuth
from django.contrib import messages
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from .forms import UpdateProfileForm
from common.models import *
from common.pagination import CustomPageNumberPagination
from inboxes.models import InboxItem, Inbox
from . import serializers
from .models import *

localHostList = [
    'http://127.0.0.1:7070/', 'http://127.0.0.1:8000/',
    'http://localhost:8000', 'http://localhost:8000/',
    'https://c404-social-distribution.herokuapp.com/'
]

connectionNodes = ConnectionNode.objects.all()


@login_required(login_url='/accounts/login')
def profile(request, user_id):
    # get basic info
    current_author_info = get_object_or_404(Author, pk=user_id)
    actor = Author.objects.filter(username=request.user.username).first()
    object = Author.objects.filter(username=user_id).first()
    # get github info
    github_username = current_author_info.github.split("/")[-1]

    posts = []

    response_contents = None
    # original UUID from Original server for current_author_info
    current_author_original_uuid = current_author_info.id.split('/')[-1]

    for node in connectionNodes:
        response = requests.get(
            f"{node.url}authors/{current_author_original_uuid}/posts/",
            params=request.GET,
            auth=HTTPBasicAuth(node.auth_username, node.auth_password))
        if response.status_code == 200:
            # TODO: Might have to accommodate for pagination once that is implemented
            posts = response.json()['items']
        else:
            pass

    # add UUID to posts object
    for post in posts:
        post['uuid'] = post['id'].split('/')[-1]

    # get follow
    if FriendFollowRequest.objects.filter(
            actor__username=actor.username,
            object__username=object.username).first():
        button_text = 'Friend Request Sent'
    else:
        button_text = 'Send Friend Request'
    user = Author.objects.get(username=user_id)
    try:
        count_followers = len(
            Followers.objects.filter(user=user)[0].items.all())
    except:
        count_followers = 0
    author_list = Author.objects.all()
    context = {
        'current_author_info': current_author_info,
        'button_text': button_text,
        'count_followers': count_followers,
        'github_username': github_username,
        'posts': posts,
        'author_list': author_list,
    }
    # breakpoint()
    return render(request, 'profile.html', context)

@login_required(login_url='/accounts/login')
def editProfile(request, user_id):
    if request.method == 'POST':
        username = request.user.username
        profile_form = UpdateProfileForm(request.POST, instance=Author.objects.filter(username=user_id).first())

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('authors:profile', user_id=username)
    else:
        profile_form = UpdateProfileForm(instance=Author.objects.filter(username=user_id).first())

    return render(request, 'editProfile.html', {'profile_form': profile_form})
    
@login_required(login_url='/accounts/login')
def follow(request):
    # TODO: maybe change name to something else instead of object?
    if request.method == 'POST':
        actorName = request.POST['follower']
        objectName = request.POST['user']
        # actor = Author.objects.filter(username=actorName).first()
        # actorName = request.user.username
        actor = Author.objects.filter(username=actorName).first()
        # object_id = request.POST.get("receiver_user_id")
        object = Author.objects.filter(username=objectName).first()
        # objectName = object.displayName

        if FriendFollowRequest.objects.filter(actor=actor, object=object):
            pass
            # delete_follower = FriendFollowRequest.objects.get(actor=actor, object=object)
            # delete_follower.delete()
            # raise Exception('Friend request canceled')
        else:
            if object.host in localHostList:
                print("following local users...", object.username)
                friendRequest = FriendFollowRequest.objects.create(
                    actor=actor,
                    object=object,
                    summary=
                    f'created request: {actorName} wants to follow {objectName}'
                )

                # when created, also push into recepients inbox
                InboxItem.objects.create(inbox=Inbox.objects.filter(
                    author__username=objectName).first(),
                                         item=friendRequest,
                                         inbox_item_type='FriendFollowRequest')

                friendRequest.save()
            else:
                friendRequest = FriendFollowRequest.objects.create(
                    actor=actor,
                    object=object,
                    summary=
                    f'created request: {actorName} wants to follow {objectName}'
                )
                friendRequest.save()
                print(f'following remote author {object.username}')

                # since author is not local, make request to remote inbox
                serializer = serializers.FriendFollowRequestSerializer(
                    friendRequest)

                objectNode = connectionNodes.filter(
                    url=f"{object.host}service/").first()
                req = requests.Request(
                    'POST',
                    f"{objectNode.url}authors/{object.username}/inbox",
                    data=json.dumps(serializer.data),
                    auth=HTTPBasicAuth(objectNode.auth_username,
                                       objectNode.auth_password),
                    headers={'Content-Type': 'application/json'})
                prepared = req.prepare()

                s = requests.Session()
                resp = s.send(prepared)
                print(f"sending remote friend request to: "\
                    f"{object.host}/service/authors/{object.username}/inbox")

                print("remote request status code, ", resp.status_code)
        return redirect('authors:profile', user_id=objectName)
    else:
        return redirect('/')


@login_required(login_url='/accounts/login')
def friendRequests(request):
    context = {}
    actorName = request.user.username
    actor = Author.objects.get(username=actorName)
    friendRequests = FriendFollowRequest.objects.filter(object=actor)
    context['friendRequests'] = friendRequests
    return render(request, 'friendRequests.html', context)


@login_required(login_url='/accounts/login')
def acceptFriendRequest(request, actor_id):
    objectName = request.user.username
    object = Author.objects.get(username=objectName)
    actor = Author.objects.get(username=actor_id)
    if request.method == 'GET':
        friendRequest_accept = FriendFollowRequest.objects.get(actor=actor,
                                                               object=object)
        if friendRequest_accept:
            if Followers.objects.filter(user=object):
                Followers.objects.get(user=object).items.add(actor)
            else:
                Followers.objects.create(user=object)
                Followers.objects.get(user=object).items.add(actor)
            return render(request, 'feed.html')


@login_required(login_url='/accounts/login')
def getuser(request):
    try:
        username = request.GET['username']
    except:
        return redirect('inboxes:postList')
    try:
        current_author_info = Author.objects.get(displayName=username)
    except:
        # if requested author is does not exist
        author_list = Author.objects.all()
        context = {
            'username': username,
            'author_list': author_list,
        }
        return render(request, 'profileNotFound.html', context)
    # if requested user exists
    user_id = current_author_info.username
    return redirect('authors:profile', user_id=user_id)


#
# API
#


class AuthorAPIView(RetrieveUpdateAPIView):
    """ GET or PUT an Author object """
    # note that PUT is updating an author object

    serializer_class = serializers.AuthorSerializer
    lookup_field = "uuid"
    http_method_names = ['get', 'put']

    def get_queryset(self):
        uuid = self.kwargs['uuid']
        return Author.objects.filter(uuid=uuid)


class AuthorsAPIView(ListAPIView):
    """ GET Authors (with pagination support)"""
    # TODO pagination failed
    # resource https://www.youtube.com/watch?v=eaWzTMtrcrE&list=PLx-q4INfd95FWHy9M3Gt6NkUGR2R2yqT8&index=9
    serializer_class = serializers.AuthorSerializer
    pagination_class = CustomPageNumberPagination
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        # breakpoint()
        url = request.build_absolute_uri('/')
        serializer = serializers.AuthorSerializer(
            Author.objects.filter(host=url), many=True)
        return Response({"type": "authors", "items": serializer.data})


# TODO rewrite FollowersAPIView
# class FollowersAPIView(RetrieveAPIView):
#     """ GET an Author's all followers """
#
#     # serializer_class = serializers.FollowersSerializer
#     # renderer_classes = (renderers.FollowersRenderer,)
#     http_method_names = ['get']
#
#     def retrieve(self, request, *args, **kwargs):
#         queryset = []
#         uuid = self.kwargs['author']
#         author = Author.objects.filter(uuid=uuid).first()
#         followers = FollowerCount.objects.filter(user=author.username)
#         for follower in followers:
#             author = model_to_dict(
#                 Author.objects.filter(username=follower.follower).first())
#             serializer = serializers.AuthorSerializer(author)
#             queryset.append(serializer.data)
#         response = {"type": "followers", "items": queryset}
#         return Response(response)

# TODO rewrite FollowerAPIView
# class FollowerAPIView(RetrieveUpdateDestroyAPIView):
#     """ GET if is a follower PUT a new follower DELETE an existing follower"""
#
#     serializer_class = serializers.FollowersSerializer
#     renderer_classes = [JSONRenderer]
#
#     def usernames(self, *args, **kwargs):
#         follower_uuid = self.kwargs['another_author']
#         follower = Author.objects.filter(uuid=follower_uuid).first()
#         user_uuid = self.kwargs['author']
#         user = Author.objects.filter(uuid=user_uuid).first()
#         return follower.username, user.username
#
#     def relation_check(self, *args, **kwargs):
#         usernames = self.usernames()
#         followers = FollowerCount.objects.filter(
#             user=usernames[1]).values_list('follower', flat=True)
#         if usernames[0] in followers:
#             return True
#         return False
#
#     def retrieve(self, request, *args, **kwargs):
#
#         if self.relation_check():
#             return Response({'following_relation_exist': 'True'})
#         else:
#             return Response({'following_relation_exist': 'False'})
#
#     def put(self, request, *args, **kwargs):
#         if self.relation_check():
#             return Response({
#                 'following_relation_exist': 'True',
#                 'following_relation_put': 'False'
#             })
#         else:
#             try:
#                 usernames = self.usernames()
#                 FollowerCount.objects.create(follower=usernames[0],
#                                              user=usernames[1])
#                 return Response({
#                     'following_relation_exist': 'False',
#                     'following_relation_put': 'True'
#                 })
#             except:
#                 return Response({
#                     'following_relation_exist': 'False',
#                     'following_relation_put': 'False'
#                 })
#
#     def delete(self, request, *args, **kwargs):
#         if self.relation_check():
#             usernames = self.usernames()
#             relation = FollowerCount.objects.filter(
#                 follower=usernames[0]).filter(user=usernames[1])
#             try:
#                 relation.delete()
#                 return Response({
#                     'following_relation_exist': 'True',
#                     'following_relation_delete': 'True'
#                 })
#             except:
#                 return Response({
#                     'following_relation_exist': 'True',
#                     'following_relation_delete': 'False'
#                 })
#         else:
#             return Response({
#                 'following_relation_exist': 'False',
#                 'following_relation_delete': 'False'
#             })
