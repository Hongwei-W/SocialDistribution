from django.contrib import admin
from .models import Author, FollowerCount, Post
#from .models import Profile


# Register your models here.
admin.site.register(Post)
admin.site.register(Author)
admin.site.register(FollowerCount)
#admin.site.register(Profile)