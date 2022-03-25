import uuid
from django.db import models
from django.utils.timezone import localtime
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Create your models here.
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


class Authors(models.Model):
    type = models.CharField(default='authors', max_length=200)
    items = models.ManyToManyField(to=Author)


class Category(models.Model):
    cat = models.CharField(max_length=50)

    def __str__(self):
        return self.cat

class Followers(models.Model):
    type = models.CharField(default='followers', max_length=200)
    user = models.OneToOneField(to=Author, 
                                on_delete=models.CASCADE,
                                related_name='user')
    items = models.ManyToManyField(to=Author,
                                related_name='items', blank=True)
    def __str__(self):
	    return self.user.username
    # def add_friend(self):
    #     pass

    

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
    def __str__(self):
        return self.actor.username
    
    def accept(self):
        Followers.objects.get(user=self.object).items.add(self.actor)
        self.delete()
		# if object_friend_list:
		# 	object_friend_list.add_friend(self.sender)
		# 	sender_friend_list = Followers.objects.get(user=self.sender)
		# 	if sender_friend_list:
		# 		sender_friend_list.add_friend(self.receiver)
		# 		self.is_active = False
		# 		self.save()


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
    CONTENT_CHOICES = [("text/plain", "Plaintext"), ("text/markdown", "Markdown"), 
                          ("application/base64", "app"), ("image/png;base64", "png"), ("image/jpeg;base64", "jpeg")]
    contentType = models.CharField(max_length=30,
                                  choices=CONTENT_CHOICES)
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE)
    unparsedCategories = models.CharField(max_length=100, default="")
    categories = models.ManyToManyField(Category)
    count = models.IntegerField(default=0)
    comments = models.TextField(default = "http://localhost:8000/")
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
    
    # def save(self, *args, **kwargs):
    #     if self.post_image:
    #         img_file = open(self.post_image.url, "rb")
    #         self.image_b64 = base64.b64encode(img_file.read())
    #         super(Image, self).save(*args, **kwargs)

class Like(models.Model):
    type = models.CharField(default='Like', max_length=200)
    # summary = models.TextField()
    # content = models.TextField()
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE)
    object = models.ForeignKey(to=Post, on_delete=models.CASCADE)


class Comment(models.Model):
    type = models.CharField(default='comment', max_length=200)
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE)
    comment = models.TextField()
    CONTENT_CHOICES = [("text/plain", "Plaintext"),("text/markdown", "Markdown")]
    contentType = models.CharField(max_length=30,
                                  choices=CONTENT_CHOICES)
    published = models.DateTimeField(default=localtime,
                                     blank=True,
                                     editable=False)
    uuid = models.UUIDField(default=uuid.uuid4,
                          editable=False,
                          unique=True,
                          primary_key=True)
    id = models.CharField(max_length=200)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, null=True)



class Liked(models.Model):
    type = models.CharField(default='liked', max_length=200)
    items = models.ManyToManyField(to=Like)


class Inbox(models.Model):
    type = models.CharField(default='inbox', max_length=200)
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE)
    items = models.ManyToManyField(to=Post)
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    # object_id = models.CharField(max_length=250, null=True)
    # content_object = GenericForeignKey('content_type', 'object_id')


