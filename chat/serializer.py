from rest_framework import serializers
from login.models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('social_login_id', 'nickname', 'profile_image')
