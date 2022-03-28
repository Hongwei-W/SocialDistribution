from django.contrib import admin
from .models import Inbox, InboxItem

# Register your models here.
admin.site.register(Inbox)
admin.site.register(InboxItem)