from user.models import User
from django.db import models
from django.utils import timezone
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=20, null=False, default='')

    class Meta:
        db_table = "category"

    def __str__(self):
        return self.name

class Board(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=200)
    text = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=50)
    price = models.IntegerField()
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    thumbnail = models.ImageField(u'썸네일',
                                  upload_to = '%Y/%m/%d', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "board"

    def __str__(self):
        Board.objects.filter(date__lte=timezone.now())\
                    .order_by('created_at')
        return self.title



