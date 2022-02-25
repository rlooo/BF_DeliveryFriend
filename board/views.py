import json

from django.views.generic import FormView, DeleteView
from django.views import View
from haversine import haversine
from rest_framework.generics import ListAPIView, get_object_or_404

from board.models import Board, Category
from board.serializer import BoardListSerializer, CategorySerializer
from user.decorators import id_auth
from user.models import Account
from django.http import HttpResponse, JsonResponse

from django.db.models import Q


# 게시물 상세 조회하는 함수
def board_detail(request, pk):
    # data = json.loads(request.body)
    # login_session = data['login_session']

    # 게시글(Post) 중 pk(primary_key)를 이용해 하나의 게시글(post)를 검색
    board = get_object_or_404(Board, id=pk)

    # # 글의 작성자인지 판별
    # if board.author.social_login_id == login_session:
    #     author_vaild = True
    # else:
    #     author_vaild = False

    return HttpResponse(json.dumps(board, indent=4, sort_keys=True, default=str),
                            content_type="application/json", status=200)


# 새로운 게시글 작성하는 함수
#@id_auth
def new_post(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        if Account.objects.filter(social_login_id=data['author']).exists():
            user = Account.objects.get(social_login_id=data['author'])

        if Category.objects.filter(id=data['category']).exists():
            category_obj = Category.objects.get(id=data['category'])

        new_article = Board.objects.create(
            author=user,
            title=data['title'],
            text=data['text'],
            date=data['date'],
            longitude=data['longitude'],
            latitude=data['latitude'],
            price=data['price'],
            category=category_obj,
            thumbnail=data['thumbnail'],
        )
        new_article.save()
        return HttpResponse(status=200)


# 게시글 삭제 기능
#@id_auth
def post_delete(request, pk):
    # data = json.loads(request.body)
    # login_session = data['login_session']
    board = get_object_or_404(Board, id=pk)
    # if board.author.social_login_id == login_session:
    board.delete()
    return HttpResponse(status=200)
    # else:
    #     return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)


# 게시글 수정 기능
#@id_auth
def post_modify(request, pk):
    #data = json.loads(request.body)
    # login_session = data['login_session']
    board = get_object_or_404(Board, id=pk)

    # if board.author.social_login_id != login_session:
    #     return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)

    if request.method == 'POST':
        data = json.loads(request.body)
        if Category.objects.filter(id=data['category']).exists():
            category_obj = Category.objects.get(id=data['category'])

        board.title = data['title']
        board.text = data['text']
        board.date = data['date']
        board.longitude = data['longitude']
        board.latitude = data['latitude']
        board.price = data['price']
        board.category = category_obj
        board.thumbnail = data['thumbnail']

        board.save()

        return HttpResponse(status=200)

# 모든 게시글들을 불러오기
class BoardListView(ListAPIView):
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


# 카테고리 리스트를 불러오기
class CategoryViewSet(ListAPIView):
    queryset = Category.objects.all()  # 카테고리 모델을 모두 부른다.
    serializer_class = CategorySerializer

    def get(self, request, format=None):
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        return HttpResponse(json.dumps(serializer.data, ensure_ascii=False, indent='\t'), status=200)


# 카테고리 별 게시글 불러오기
class CategorySearchViewSet(View):
    def get(self, request, id):
        queryset = Board.objects.filter(category__id=id)
        serializer = BoardListSerializer(queryset, many=True)
        return HttpResponse(json.dumps(serializer.data, ensure_ascii=False, indent='\t'), status=200)


# 검색 기능
class SearchView(View):
    def get(self, request):
        data = json.loads(request.body)
        search_word = data['search_word']

        post_list = Board.objects.filter(Q(title__icontains=search_word) | Q(text__icontains=search_word)).distinct().values()

        # return HttpResponse(json.dumps(post_list, indent=4, sort_keys=True, default=str),
        #                     content_type="application/json", status=200)
        queryset = post_list
        serializer_class = BoardListSerializer

        serializer = serializer_class(queryset, many=True)

        return HttpResponse(json.dumps(serializer.data, ensure_ascii=False, indent='\t'), status=200)

# 내 동네와 가까운 게시물 리스트 불러오기
class NearInfoListView(View):
    def get(self, request):
        data = json.loads(request.body)
        # 쿼리로 위치 정보를 받아 position이라는 변수에 저장한다.
        longitude = float(data['longitude'])
        latitude = float(data['latitude'])
        position = (latitude, longitude)

        # 반경 2km를 기준으로 정보를 불러올 것이므로 사방 1km 씩 자름 (사전 필터링으로 쿼리 속도 줄임)
        condition = (
                Q(latitude__range=(latitude - 0.01, latitude + 0.01)) |
                Q(longitude__range=(longitude - 0.015, longitude + 0.015))
        )
        # 필터를 게시물에 적용
        post_infos = (
            Board
                .objects
                .filter(condition)
        )
        # 필터된 객체와 특정 위치와의 거리가 2km 이내인 객체를 모아서 반환
        near_post_infos = [info for info in post_infos
                           if haversine(position, (info.latitude, info.longitude)) <= 2]

        queryset = near_post_infos
        serializer_class = BoardListSerializer

        serializer = serializer_class(queryset, many=True)

        return HttpResponse(json.dumps(serializer.data, ensure_ascii=False, indent='\t'), status=200)