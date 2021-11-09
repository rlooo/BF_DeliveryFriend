from login.models import Account
from django.db import models
from django.utils import timezone
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=20, null=False, default='')
    def __str__(self):
        return self.name

class Board(models.Model):
    author = models.ForeignKey(Account, on_delete=models.DO_NOTHING, null=True)
    title = models.CharField(max_length=200)
    text = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=50)
    price = models.IntegerField()
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    thumbnail = models.ImageField(u'썸네일',
                                  upload_to = '%Y/%m/%d', blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        Board.objects.filter(date__lte=timezone.now())\
                    .order_by('created_date')
        return self.title

