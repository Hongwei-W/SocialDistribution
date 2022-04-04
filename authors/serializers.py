from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from . import models


class AuthorSerializer(ModelSerializer):

    class Meta:
        model = models.Author
        fields = ('type', 'id', "host", "displayName", "github", "url",
                  "profileImage")

        
class FollowersSerializer(ModelSerializer):

    class Meta:
        model = models.FollowerCount
        fields = '__all__'


class FriendFollowRequestSerializer(ModelSerializer):
    actor = AuthorSerializer()
    object = AuthorSerializer()

    class Meta:
        model = models.FriendFollowRequest
        # fields = '__all__'
        fields = ("type", "summary", "actor", "object")
        depth = 1
