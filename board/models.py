from user.models import Account
from django.db import models
from django.utils import timezone
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=20, null=False, default='')

    class Meta:
        db_table = "category"

    def __str__(self):
        return self.name

# class Location(models.Model):
#     longitude = models.DecimalField(max_digits=9, decimal_places=6)
#     latitude = models.DecimalField(max_digits=9, decimal_places=6)
#
#     class Meta:
#         db_table = 'location'

class Board(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=200)
    text = models.TextField()
    date = models.DateTimeField()
    longitude = models.DecimalField(max_digits=25, decimal_places=20)
    latitude = models.DecimalField(max_digits=25, decimal_places=20)
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


