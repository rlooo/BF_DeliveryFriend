from rest_framework import serializers
from .models import Category, Board

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)

# 화면에서 보여줄 필드 명시
class BoardListSerializer(serializers.ModelSerializer):
    # post내에서 category가 Foreginekey이므로 id로 나타나게 되므로 아래와 같이 추가
    category = CategorySerializer(many=False, read_only=True)
    class Meta:
        model = Board
        fields = ('id', 'author', 'title', 'text', 'date', 'location', 'price', 'category', 'thumbnail', 'created_date')
