from django.db import models

from django.shortcuts import redirect
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.

class Account(models.Model):
    social_login_id = models.IntegerField(blank=True)
    email = models.CharField(max_length=100, null=True)
    nickname = models.CharField(max_length=20, null=True)
    profile_image = models.CharField(max_length=2000, null=True)

    class Meta:
        db_table = 'accounts'
