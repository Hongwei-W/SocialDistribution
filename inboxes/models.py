from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from posts.models import Post


class Inbox(models.Model):
    type = models.CharField(default='inbox', max_length=200)
    author = models.ForeignKey(to="authors.Author", on_delete=models.CASCADE)
    items = models.ManyToManyField(to=Post)

    # for reverse lookup of inbox items
    # https://stackoverflow.com/questions/15306897/django-reverse-lookup-of-foreign-keys

    def __str__(self) -> str:
        return f"{self.author.username}'s inbox"

    def to_dict(self):
        return {
            'type': self.type,
            'author': self.author.username,
            # 'items_object': self.items_object.to_dict()
        }


class InboxItem(models.Model):
    inbox = models.ForeignKey(to=Inbox, on_delete=models.CASCADE)
    # model field in choices {like, post, comment, friendfollowrequest}
    choices = [("like", "like"), ("post", "post"), ("comment", "comment"),
               ("follow", "follow")]
    inbox_item_type = models.CharField(max_length=20, choices=choices)

    # if inbox item is read
    is_read = models.BooleanField(default=False)

    # GFK to {like, post, comment, friendfollowrequest}
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255)
    item = GenericForeignKey('content_type', 'object_id')

    def __str__(self) -> str:
        return f"{self.inbox.author.username}'s {self.inbox_item_type}: {self.content_type}, {self.object_id}"

    def to_dict(self) -> dict:
        return {
            'inbox_item_type': self.inbox_item_type,
            'content_type': self.content_type,
            'object_id': self.object_id,
            'item': self.item.to_dict()
        }
