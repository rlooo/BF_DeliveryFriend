from django.db import models


from django.shortcuts import redirect
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.
class Information(models.Model):
    name = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=13)
    createAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['createAt']

class Account(models.Model):
    social_login_id = models.IntegerField(blank=True)
    email = models.CharField(max_length=60, null=True)
    nickname = models.CharField(max_length=20)
    profile_image = models.CharField(max_length=2000)
