from django.forms import model_to_dict
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from authors.models import Author, FriendFollowRequest
from authors.serializers import FriendFollowRequestSerializer
from posts.models import Comment, Like, Post
from posts.serializers import PostSerializer, LikesSerializer, CommentsSerializer
from .models import Inbox


class InboxSerializer(ModelSerializer):
    author = serializers.SerializerMethodField('get_author')
    items = serializers.SerializerMethodField('get_items')

    class Meta:
        model = Inbox
        fields = ('type', "author", "items")
        depth = 1

    def get_author(self, obj):
        author_username = obj.to_dict().get("author")
        author = Author.objects.filter(username=author_username).first()
        return model_to_dict(author).get("id")

    def get_items(self, obj):
        inbox = obj  # obj is inbox object
        # get items from the inbox
        # for each item call its serializer method
        # return the serialized items
        items = inbox.inboxitem_set.all()
        itemArray = []
        for item in items:
            if item.inbox_item_type == "post":
                postObject = Post.objects\
                    .filter(uuid=item.object_id).first()
                itemArray.append(PostSerializer(postObject).data)

            elif item.inbox_item_type == "comment":
                commentObject = Comment.objects\
                    .filter(uuid=item.object_id).first()
                itemArray.append(CommentsSerializer(commentObject).data)

            elif item.inbox_item_type == "like":
                likeObject = Like.objects\
                    .filter(id=item.object_id).first()
                itemArray.append(LikesSerializer(likeObject).data)

            elif item.inbox_item_type == "friend_follow_request":
                friendFollowRequestObject = FriendFollowRequest.objects\
                    .filter(id=item.object_id).first()
                itemArray.append(
                    FriendFollowRequestSerializer(friendFollowRequestObject)\
                        .data)
        return itemArray
