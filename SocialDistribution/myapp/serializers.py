from rest_framework.serializers import ModelSerializer
from . import models

class AuthorSerializer(ModelSerializer):

    class Meta:
        model = models.Author
        fields = '__all__'

# class SingleAuthorSerializer(ModelSerializer):
#
#     class Meta:
#         model = models.Author
#         fields = '__all__'


class FollowersSerializer(ModelSerializer):

    class Meta:
        model = models.FollowerCount
        fields = '__all__'


# class FriendFollowRequestSerializer(ModelSerializer):
#
#     class Meta:
#         model = models.FriendFollowRequest
#         fields = '__all__'


class PostSerializer(ModelSerializer):
    class Meta:
        model = models.Post
        fields = '__all__'

# class ImagePostSerializer(ModelSerializer):
#
#     # TODO image post & model
#     class Meta:
#         model = models.Post
#         fields = ''

class CommentSerializer(ModelSerializer):

    class Meta:
        model = models.Comment
        fields = '__all__'

# class LikeSerializer(ModelSerializer):
#
#     class Meta:
#         model = models.Like
#         fields = '__all__'

# class LikedSerializer(ModelSerializer):
#
#     class Meta:
#         model = models.Liked
#         fields = '__all__'


# class InboxSerializer(ModelSerializer):
#     class Meta:
#         model = models.Inbox
#         fields = '__all__'



