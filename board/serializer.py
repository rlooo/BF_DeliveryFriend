from rest_framework import serializers
from .models import Category, Board

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)

class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('id', 'author', 'title', 'date', 'location', 'price', 'created_date')