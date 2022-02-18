from rest_framework import serializers
from user.models import Account

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('social_login_id', 'nickname', 'profile_image')
