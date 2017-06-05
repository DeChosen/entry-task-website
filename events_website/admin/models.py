from django.db import models


class user(models.Model):
    username = models.CharField(max_length=254, null=False, blank=True)
    password = models.CharField(max_length=254, null=False, blank=True)
    type = models.CharField(default='user', max_length=10, editable=False)

    def __unicode__(self):
        return self.username
