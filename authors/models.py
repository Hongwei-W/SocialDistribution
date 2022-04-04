from tabnanny import verbose
import uuid

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models


class Author(models.Model):
    type = models.CharField(default="author", max_length=200)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=True)
    id = models.CharField(max_length=200)
    username = models.CharField(unique=True, max_length=200, primary_key=True)
    host = models.CharField(max_length=200)
    displayName = models.CharField(max_length=200, null=True)
    github = models.CharField(max_length=200, null=True)
    profileImage = models.CharField(max_length=500, null=True, blank=True)
    url = models.CharField(max_length=200)

    def __str__(self):
        return self.username

    def to_dict(self):
        return {
            'uuid': str(self.uuid),
            'id': self.id,
            'username': self.username,
            'host': self.host,
            'displayName': self.displayName,
            'github': self.github,
            'profileImage': self.profileImage,
            'url': self.url,
        }


class Followers(models.Model):
    type = models.CharField(default='followers', max_length=200)
    user = models.OneToOneField(to=Author,
                                on_delete=models.CASCADE,
                                related_name='user')
    items = models.ManyToManyField(to=Author, related_name='items', blank=True)

    class Meta:
        verbose_name = 'Follower'
        verbose_name_plural = 'Followers'

    def __str__(self):
        return self.user.username

    def to_dict(self):
        return {
            'type': self.type,
            'users_following': self.items,
            'user_followed': self.user,
        }


class FollowerCount(models.Model):
    # follower is who logged in now # user.usernamr
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user


class FriendFollowRequest(models.Model):
    type = models.CharField(default='follow', max_length=200)
    summary = models.TextField()
    actor = models.ForeignKey(to=Author,
                              on_delete=models.CASCADE,
                              related_name='%(class)s_request_sender')
    object = models.ForeignKey(to=Author,
                               on_delete=models.CASCADE,
                               related_name='%(class)s_request_receiver')
    inbox = GenericRelation("inboxes.InboxItem")


    def accept(self):
        Followers.objects.get(user=self.object).items.add(self.actor)
        self.delete()

    def __str__(self):
        return self.actor.username

    def to_dict(self):
        return {
            'summary': self.summary,
            'actor': self.actor.username,
            'object': self.object.username,
            'type': self.type,
        }