import json

from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework import generics
from rest_framework.views import APIView
from django.views import View

from login.models import Account
from .models import Category, Board
from .serializer import CategorySerializer, BoardListSerializer
from django.http import HttpResponse, JsonResponse
# Create your views here.

class CategoryViewSet(APIView):
    def get(self, request, format=None):
        queryset = Category.objects.all() # 카테고리 모델을 모두 부른다.
        serializer = CategorySerializer(queryset, many=True)
        return HttpResponse(serializer.data)

@method_decorator(csrf_exempt, name='dispatch')
# 새로운 게시글 작성하는 함수
class BoardPostingView(View):
    def post(self, request):
        if request.method == 'POST':
            form = BoardListSerializer(data=request.POST)

            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.author
                post.title = request.title
                post.date = request.date
                post.location = request.location
                post.price = request.price
                post.category = request.category
                post.thumbnail = request.thumbnail
                post.save()
                return HttpResponse(status=200)

            return HttpResponse(status=400)


# 모든 게시글들을 불러오는 함수
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

        return HttpResponse(serializer.data, status=200)