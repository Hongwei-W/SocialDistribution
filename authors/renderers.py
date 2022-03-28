import json

from rest_framework import renderers


class AuthorsRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        data["type"] = "authors"
        data.move_to_end("type", last=False)
        response = json.dumps(data)

        return response


# class FollowersRenderer(renderers.JSONRenderer):
#     charset = 'utf-8'
#
#     def render(self, data, accepted_media_type=None, renderer_context=None):
#
#         response = json.dumps({"type": "followers", "items": dict(data).get("results")})
#
#         return response
