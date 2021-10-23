from rest_framework import serializers
from .models import Category, Board

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)

# 화면에서 보여줄 필드 명시
class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('id', 'author', 'title', 'date', 'location', 'price', 'created_date')