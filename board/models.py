from django.db import models
from django.utils import timezone
from __future__ import unicode_literals

# Create your models here.
class Board(models.Model):
    author = models.ForeignKey('login.Account')
    title = models.CharField(max_length=200)
    text = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=50)
    price = models.IntegerField()
    category = models.ForeignKey('Category', null=True, blank=True)
    thumbnail = models.ImageField(u'썸네일',
                                  upload_to = '%Y/%m/%d', blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)


class Category(models.Model):
    name = models.CharField