from django.contrib import admin
from .models import ConnectionNode, ServerSetting

# Register your models here.
class ConnectionNodeAdmin(admin.ModelAdmin):
    list_display = ['name', 'url']


class ServerSettingAdmin(admin.ModelAdmin):
    list_display = ['type', 'allow_independent_user_login']


admin.site.register(ConnectionNode, ConnectionNodeAdmin)
admin.site.register(ServerSetting, ServerSettingAdmin)
