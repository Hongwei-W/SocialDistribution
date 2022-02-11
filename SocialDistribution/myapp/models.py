from email.policy import default
from xml.etree.ElementInclude import default_loader
from django.db import models
from torch import true_divide


# Create your models here.
class Author(models.Model):
    type = models.CharField(default="author")
    id = models.CharField(unique=True, max_length=200, primary_key=True)
    host = models.CharField(max_length=200)
    displayName = models.CharField(max_length=200)
    github = models.TextField()
    profileImage = models.TextField()


class Authors(models.Model):
    type = models.CharField(default='authors')
    items = models.ManyToManyField(to=Author)


class Followers(models.Model):
    type = models.CharField(default='followers')
    items = models.ManyToManyField(to=Author)


class FriendFollowRequest(models.Model):
    type = models.CharField(default='Follow')
    summary = models.TextField()
    actor = models.ForeignKey(to=Author)
    object = models.ForeignKey(to=Author)


class Post(models.Model):
    type = models.CharField(default='post')
    title = models.CharField()
    id = models.CharField(unique=True, max_length=200, primary_key=True)
    source = models.Charfield()
    origin = models.CharField()
    description = models.TextField()
    contentType = models.Charfield()
    author = models.ForeignKey(to=Author)
    categories = models.TextField()
    count = models.IntegerField
    comments = models.CharField()
    commentsSrc = models.ForeignKey(to=Comment)
    published = models.DateField()
    visiblity = models.CharField()
    unlisted = models.BooleanField()


class Comment(models.Model):
    type = models.CharField(default='comment')
    author = models.ForeignKey(to=Author)
    comment = models.TextField()
    contentType = models.Charfield()
    published = models.DateField()
    id = models.CharField(unique=True, max_length=200, primary_key=True)


class Like(models.Model):
    type = models.CharField(default='Like')
    summary = models.TextField()
    content = models.CharField()
    author = models.ForeignKey(to=Author)
    object = models.ForeignKey(to=Post)


class Liked(models.Model):
    type = models.CharField(default='liked')
    items = models.ManyToManyField(to=Post)


class Inbox(models.Model):
    type = models.CharField(default='inbox')
    author = models.ForeignKey(to=Authors)
    items = models.ManyToManyField(to=Post)