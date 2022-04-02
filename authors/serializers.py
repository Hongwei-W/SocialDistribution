from rest_framework.serializers import ModelSerializer

from . import models


class AuthorSerializer(ModelSerializer):

    class Meta:
        model = models.Author
        fields = ('type', 'id', "host", "displayName", "github",
                  "profileImage")


class FollowersSerializer(ModelSerializer):

    class Meta:
        model = models.FollowerCount
        fields = '__all__'


class FriendFollowRequestSerializer(ModelSerializer):

    class Meta:
        model = models.FriendFollowRequest
        # fields = '__all__'
        fields = ("type", "summary", "actor", "object")
        depth = 1
