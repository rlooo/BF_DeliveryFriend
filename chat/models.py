from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder

class Room(models.Model):
    name = models.TextField()
    label = models.SlugField(unique=True)

    def __unicode__(self):
        return self.label

class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.SET_NULL, null=True)
    senderId = models.TextField(null=True)
    receiverId = models.TextField(null=True)
    message = models.TextField(null=True)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    def __unicode__(self):
        return '[{timestamp}] {senderId} {receiverId}: {message}'.format(**self.as_dict())

    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime('%b %-d %-I:%M %p')

    def as_dict(self):
        return {'senderId': self.senderId, 'receiverId': self.receiverId, 'message': self.message, 'timestamp': self.formatted_timestamp}

