from django.db import models

# Create your models here.


class ConnectionNode(models.Model):
    """
        Class to contain the connection node information of other
        nodes
        url INCLUDES the backslash at the end
    """
    name = models.CharField(max_length=255)
    url = models.URLField()
    auth_username = models.CharField(max_length=255)
    auth_password = models.CharField(max_length=255)

    class Meta:
        verbose_name = "connection node"
        verbose_name_plural = "connection nodes"

    def __str__(self):
        return str(self.name)

    def to_dict(self):
        return {
            'name': self.name,
            'url': self.url,
            'auth_username': self.auth_username,
            'auth_password': self.auth_password
        }