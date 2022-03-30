from django.contrib import admin
from .models import *

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    # https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Admin_site
    list_filter = ['author__username']
    list_display = ('title', 'author', 'published')


admin.site.register(Post, PostAdmin)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Category)