from django.forms import model_to_dict
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from authors.serializers import AuthorSerializer
from . import models
from .models import Post


class PostSerializer(ModelSerializer):
    author = AuthorSerializer()
    categories = serializers.SerializerMethodField('get_categories')

    def get_categories(self, obj):
        post = model_to_dict(obj)
        categories = post.get("categories")
        lst = []
        for i in categories:
            category = model_to_dict(i)
            lst.append(category.get("cat"))
        return lst

    class Meta:
        model = models.Post
        fields = ("type", "title", "id", "source", "origin", "description",
                  "content", "contentType", "author", "categories", "count",
                  "comments", "published", "visibility", "unlisted", "likes",
                  "image_b64")
        depth = 1


class CommentsSerializer(ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = models.Comment
        fields = ("type", "author", "comment", "contentType", "published",
                  "id")


class LikesSerializer(ModelSerializer):
    author = AuthorSerializer()
    # object = serializers.SerializerMethodField('get_object')

    class Meta:
        model = models.Like
        fields = ("type", "author", "object", "summary")

    # def get_object(self, obj):
    #     like = model_to_dict(obj)
    #     post_uuid = like.get("object")
    #     post = Post.objects.filter(uuid=post_uuid).first()
    #     return model_to_dict(post).get("id")
