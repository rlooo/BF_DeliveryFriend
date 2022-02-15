from django.db import models

from django.shortcuts import redirect
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.

class User(models.Model):
    social_login_id = models.IntegerField(null=False, blank=False, unique=True)
    email = models.EmailField(max_length=100, null=True)
    nickname = models.CharField(max_length=20, unique=True)
    profile_image = models.CharField(max_length=2000, null=True, blank=True)
    #address = models.ManyToManyField(null=True) # 추후에 null=True 해제
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'user'

    # def __str__(self):
    #     return self.social_login_id

class Address(models.Model):
    address = models.CharField(max_length=20, null=False)
    code = models.IntegerField()
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'address'
