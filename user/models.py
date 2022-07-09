from django.db import models


# Create your models here.

class Account(models.Model):
    social_login_id = models.IntegerField(null=False, blank=False, unique=True)
    email = models.EmailField(max_length=100, null=True)
    nickname = models.CharField(max_length=20, unique=True)
    profile_image = models.CharField(max_length=2000, null=True, blank=True,
                                     default='https://png.pngtree.com/element_our/20200610/ourlarge/pngtree-character-default-avatar-image_2237203.jpg')
    longitude = models.CharField(max_length=200, null=True, blank=True) # 경도
    latitude = models.CharField(max_length=200, null=True, blank=True) # 위도
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'user'

    # def __str__(self):
    #     return self.social_login_id


# class Address(models.Model):
#     user = models.ForeignKey('Account', related_name='address', on_delete=models.CASCADE, )
#     code = models.IntegerField()
#
#     created_at = models.DateTimeField(auto_now_add=True)
#     deleted_at = models.DateTimeField(null=True)
#
#     class Meta:
#         db_table = 'address'
