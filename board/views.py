from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView

from .models import Category, Board
from .serializer import CategorySerializer, BoardListSerializer
from django.http import HttpResponse, JsonResponse
# Create your views here.

class CategoryViewSet(APIView):
    def get(self, request, format=None):
        queryset = Category.objects.all() # 카테고리 모델을 모두 부른다.
        serializer = CategorySerializer(queryset, many=True)
        return HttpResponse(serializer.data)

#n
class BoardListView(generics.ListAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardListSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return HttpResponse(serializer.data)