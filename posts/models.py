import uuid

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.timezone import localtime
from django.contrib import admin


class Category(models.Model):
    cat = models.CharField(max_length=50)

    def __str__(self):
        return self.cat


class Post(models.Model):
    type = models.CharField(default='post', max_length=200)
    title = models.CharField(max_length=200)
    uuid = models.UUIDField(default=uuid.uuid4,
                            editable=True,
                            unique=True,
                            primary_key=True)
    id = models.CharField(max_length=200)
    source = models.CharField(max_length=200)
    origin = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField()
    CONTENT_CHOICES = [("text/plain", "Plaintext"),
                       ("text/markdown", "Markdown"),
                       ("application/base64", "app"),
                       ("image/png;base64", "png"),
                       ("image/jpeg;base64", "jpeg")]
    contentType = models.CharField(max_length=30, choices=CONTENT_CHOICES)
    author = models.ForeignKey(to="authors.Author", on_delete=models.CASCADE)
    unparsedCategories = models.CharField(max_length=100, default="")
    categories = models.ManyToManyField(Category)
    count = models.IntegerField(default=0)
    comments = models.TextField(default="http://localhost:8000/")
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
    unlisted = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)
    post_image = models.ImageField(null=True, blank=True, upload_to='images/')
    image_b64 = models.BinaryField(blank=True, null=True)
    inbox = GenericRelation("inboxes.InboxItem")
    # def save(self, *args, **kwargs):
    #     if self.post_image:
    #         img_file = open(self.post_image.url, "rb")
    #         self.image_b64 = base64.b64encode(img_file.read())
    #         super(Image, self).save(*args, **kwargs)

class Like(models.Model):
    type = models.CharField(default='like', max_length=200)
    summary = models.TextField()
    # content = models.TextField()
    author = models.ForeignKey(to="authors.Author", on_delete=models.CASCADE)
    object = models.ForeignKey(to=Post, on_delete=models.CASCADE)
    inbox = GenericRelation("inboxes.InboxItem")


class Comment(models.Model):
    type = models.CharField(default='comment', max_length=200)
    id = models.CharField(max_length=200)
    author = models.ForeignKey(to="authors.Author", on_delete=models.CASCADE)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, null=True)
    comment = models.TextField()
    CONTENT_CHOICES = [("text/plain", "Plaintext"),
                       ("text/markdown", "Markdown")]
    contentType = models.CharField(max_length=30, choices=CONTENT_CHOICES)
    published = models.DateTimeField(default=localtime,
                                     blank=True,
                                     editable=False)
    uuid = models.UUIDField(default=uuid.uuid4,
                            editable=False,
                            unique=True,
                            primary_key=True)
    inbox = GenericRelation("inboxes.InboxItem")
