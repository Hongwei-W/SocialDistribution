import uuid

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models


class Author(models.Model):
    type = models.CharField(default="author", max_length=200)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=True)
    id = models.CharField(max_length=200)
    username = models.CharField(unique=True, max_length=200, primary_key=True)

    # id = models.UUIDField(default=uuid.uuid4,
    #                       editable=False,
    #                       unique=True,
    #                       primary_key=True)
    host = models.CharField(max_length=200)
    displayName = models.CharField(max_length=200, null=True)
    github = models.CharField(max_length=200, null=True)
    profileImage = models.CharField(max_length=500, null=True, blank=True)


class Followers(models.Model):
    type = models.CharField(default='followers', max_length=200)
    user = models.OneToOneField(to=Author,
                                on_delete=models.CASCADE,
                                related_name='user')
    items = models.ManyToManyField(to=Author, related_name='items', blank=True)

    def to_dict(self):
        return {
            'type': self.type,
            'users_following': self.items,
            'user_followed': self.user,
        }

    def __str__(self):
        return self.user.username


class FollowerCount(models.Model):
    # follower is who logged in now # user.usernamr
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user


class FriendFollowRequest(models.Model):
    type = models.CharField(default='Follow', max_length=200)
    summary = models.TextField()
    actor = models.ForeignKey(to=Author,
                              on_delete=models.CASCADE,
                              related_name='%(class)s_request_sender')
    object = models.ForeignKey(to=Author,
                               on_delete=models.CASCADE,
                               related_name='%(class)s_request_receiver')
    inbox = GenericRelation("inboxes.InboxItem")

    def __str__(self):
        return self.actor.username

    def accept(self):
        Followers.objects.get(user=self.object).items.add(self.actor)
        self.delete()
