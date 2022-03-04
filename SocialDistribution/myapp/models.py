import uuid
from django.db import models
from django.utils.timezone import localtime


# Create your models here.
class Author(models.Model):
    type = models.CharField(default="author", max_length=200)
    id = models.CharField(unique=True, max_length=200, primary_key=True)

    # id = models.UUIDField(default=uuid.uuid4,
    #                       editable=False,
    #                       unique=True,
    #                       primary_key=True)
    host = models.CharField(max_length=200)
    displayName = models.CharField(max_length=200, null=True)
    github = models.CharField(max_length=200, null=True)
    profileImage = models.CharField(max_length=500, null=True, blank=True)


class Authors(models.Model):
    type = models.CharField(default='authors', max_length=200)
    items = models.ManyToManyField(to=Author)


# class Followers(models.Model):
#     type = models.CharField(default='followers', max_length=200)
#     items = models.ManyToManyField(to=Author)


class FriendFollowRequest(models.Model):
    type = models.CharField(default='Follow', max_length=200)
    summary = models.TextField()
    actor = models.ForeignKey(to=Author,
                              on_delete=models.CASCADE,
                              related_name='%(class)s_request_sender')
    object = models.ForeignKey(to=Author,
                               on_delete=models.CASCADE,
                               related_name='%(class)s_request_receiver')


class Post(models.Model):
    type = models.CharField(default='post', max_length=200)
    title = models.CharField(max_length=200)
    id = models.UUIDField(default=uuid.uuid4,
                          editable=True,
                          unique=True,
                          primary_key=True)
    # TODO: source and origin for webservices??
    # source = models.CharField(max_length=200)
    # origin = models.CharField(max_length=200)
    description = models.TextField()
    CONTENT_CHOICES = [("md", "text/markdown"), ("plain", "text/plain"),
                          ("app", "application/base64"), ("png", "image/png;base64"), ("jpeg","image/jpeg;base64")]
    contentType = models.CharField(max_length=30,
                                  choices=CONTENT_CHOICES,
                                  default="md")
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE)
    # TODO: categories as a list of strings
    categories = models.TextField()
    count = models.IntegerField(default=0)
    # TODO: comments for webservice??
    # comments = models.TextField()
    # commentsSrc = models.ForeignKey(to=Comment, on_delete=models.CASCADE)
    published = models.DateTimeField(default=localtime,
                                     blank=True,
                                     editable=False)
    # TO-DO: check if "private" is needed
    VISIBILITY_CHOICES = [("PUBLIC", "Public"), ("FRIENDS", "Friends"),
                          ("PRIVATE", "Specific friend")]
    visibility = models.CharField(max_length=7,
                                  choices=VISIBILITY_CHOICES,
                                  default="PUBLIC")
    # unlisted = models.BooleanField()
    post_image = models.ImageField(null=True, blank=True, upload_to='images/')


class Like(models.Model):
    type = models.CharField(default='Like', max_length=200)
    summary = models.TextField()
    content = models.TextField()
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE)
    object = models.ForeignKey(to=Post, on_delete=models.CASCADE)


class Comment(models.Model):
    type = models.CharField(default='comment', max_length=200)
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE)
    comment = models.TextField()
    contentType = models.CharField(max_length=200)
    published = models.DateTimeField(default=localtime,
                                     blank=True,
                                     editable=False)
    id = models.UUIDField(default=uuid.uuid4,
                          editable=False,
                          unique=True,
                          primary_key=True)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, null=True)



class Liked(models.Model):
    type = models.CharField(default='liked', max_length=200)
    items = models.ManyToManyField(to=Post)


class Inbox(models.Model):
    type = models.CharField(default='inbox', max_length=200)
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE)
    items = models.ManyToManyField(to=Post)


class FollowerCount(models.Model):
    # follower is who logged in now
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user