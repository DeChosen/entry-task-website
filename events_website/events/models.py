from django.db import models

class event(models.Model):
    name = models.CharField(max_length = 100, null = False, blank = True)
    location = models.CharField(max_length = 200, null = True, blank = True)
    date = models.DateField()
    description = models.TextField(null = True)

    def __unicode__(self):
        return self.name

class event_participants(models.Model):
    event_id = models.IntegerField()
    participant_name = models.CharField(max_length = 100, null = False, blank =True)

    def __unicode__(self):
        return self.participant_name

class event_like(models.Model):
    event_id = models.IntegerField()
    liker_name = models.CharField(max_length=100, null=False, blank=True)

    def __unicode__(self):
        return self.liker_name

class event_comments(models.Model):
    event_id = models.IntegerField()
    commenter_name = models.CharField(max_length=100, null=False, blank=True)
    comment = models.TextField(null = False)
    date = models.IntegerField()

class event_tags(models.Model):
    event_id = models.IntegerField()
    tag = models.CharField(max_length=50, null=False, blank=True)

class Photo(models.Model):
    image = models.CharField(max_length=50, null = False)
    event_id = models.IntegerField(default = 1)
