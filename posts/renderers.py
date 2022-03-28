import json

from django.forms import model_to_dict
from django.http import HttpResponseNotFound, HttpResponse
from rest_framework import renderers

from authors.models import Author


class PostsRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        results = dict(data).get("items")
        response = []
        for post in results:
            post = dict(post)

            username = post.get("author")
            author = Author.objects.filter(id=username).first()
            author = model_to_dict(author)
            post["author"] = author
            response.append(post)

        response = json.dumps({"type": "posts", "page": data["page"], "size": data["size"], "next": data["next"], "previous": data["previous"], "items": response})

        return response


class ImagePostRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        post = dict(data)

        if post.get("contentType") == "image/jpeg;base64" or post.get("contentType") == "image/png;base64":
            # username = post.get("author")
            # author = Author.objects.filter(id=username).first()
            # author = model_to_dict(author)
            # post["author"] = author
            return json.dumps(post)
        else:
            return HttpResponseNotFound('This is not an Image Post')


class CommentsRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        results = dict(data).get("items")
        try:
            post = results[0]["post"]
        except:
            return HttpResponse("This post have no comments")
        response = []
        for comment in results:
            comment = dict(comment)

            username = comment.get("author")
            author = Author.objects.filter(id=username).first()
            author = model_to_dict(author)
            comment["author"] = author
            comment["id"] = str(comment["id"])
            comment["post"] = str(comment["post"])
            response.append(comment)

        response = json.dumps({"type": "comments", "page": data["page"], "size": data["size"], "post": str(post), "id": str(post), "next": data["next"], "previous": data["previous"], "items": response})

        return response


class LikesRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        results = dict(data).get("items")
        object_id = results[0]["object"]
        response = []
        for like in results:
            like = dict(like)

            username = like.get("author")
            author = Author.objects.filter(id=username).first()
            author = model_to_dict(author)
            like["author"] = author
            like["object"] = str(like["object"])
            response.append(like)

        response = json.dumps({"type": "likes", "page": data["page"], "size": data["size"], "object": str(object_id), "next": data["next"], "previous": data["previous"], "items": response})

        return response


class LikedRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        results = dict(data).get("items")
        response = []
        for like in results:
            like = dict(like)

            username = like.get("author")
            author = Author.objects.filter(id=username).first()
            author = model_to_dict(author)
            like["author"] = author
            like["object"] = str(like["object"])
            response.append(like)

        response = json.dumps({"type": "liked", "page": data["page"], "size": data["size"], "next": data["next"], "previous": data["previous"], "items": response})

        return response
