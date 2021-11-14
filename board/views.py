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
from .serializer import *
from django.http import HttpResponse, JsonResponse

class CategoryViewSet(APIView):
    def get(self, request, format=None):
        queryset=Category.objects.all()#카테고리 모델을 모두 부른다.
        serializer_class = CategorySerializer

        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()

        serializer = serializer_class(queryset, many=True)
        return HttpResponse(serializer.data, status=200)

# # board.html 페이지를 부르는 index 함수
# def index(request):
#     return render(request, 'board/board.html')
#
# # blog.html 페이지를 부르는 blog 함수
# def post_list(request):
#     if request.method == 'GET':
#         # 모든 Board를 가져와 postlist에 저장한다.
#         postlist = Board.objects.all()
#         return HttpResponse(postlist, status=200)
#
# # blog의 게시글(posting)을 부르는 posting 함수
# def posting(request, pk):
#     # 게시글(Post) 중 pk(primary_key)를 이용해 하나의 게시글(post)를 검색
#     post = Board.objects.get(pk=pk)
#     # posting.html 페이지를 열 때, 찾아낸 게시글(post)을 post라는 이름으로 가져옴
#     return HttpResponse({'post':post},status=200)


# 새로운 게시글 작성하는 함수
def new_post(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        if Account.objects.filter(social_login_id=data['author']).exists():
            user = Account.objects.get(social_login_id=data['author'])
        print(user)
        new_article=Board.objects.create(
            author=user,
            title=data['title'],
            text=data['text'],
            date=data['date'],
            location=data['location'],
            price=data['price'],
            category=data['category'],
            thumbnail=data['thumbnail'],
        )
        new_article.save()
        return HttpResponse(status=200)

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

        return HttpResponse(json.dumps(serializer.data, ensure_ascii=False, indent='\t'), status=200)