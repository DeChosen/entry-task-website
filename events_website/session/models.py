from django.db import models
import time
from django.shortcuts import HttpResponseRedirect

class Session(models.Model):
    sessionid = models.CharField(max_length=32)
    time_created = models.IntegerField(default = time.mktime(time.localtime()))
    username = models.CharField(max_length=100)


def expired(t_now, t_created, difference):
    return t_now - t_created >= difference

def delete_session(sessionid):
    Session.objects.filter(sessionid = sessionid).delete()

def logout(sessionid):
    delete_session(sessionid)
    return HttpResponseRedirect('/login/')