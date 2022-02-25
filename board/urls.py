from django.urls import path

from board import views
from board.views import *

app_name = 'board'
urlpatterns = [

    # Example: /board/search/
    path('search/', views.SearchView.as_view(), name='post_search'),

    # Example: /board/new_post/
    path('new_post/', new_post, name='new_post'),

    # Example: /board/list/
    path('list/', BoardListView.as_view(), name='post_list'),

    # Example: /board/1/detail/
    path('<int:pk>/detail/', views.board_detail, name="post_detail"),

    # Example: /board/change/
    #path('change/', views.PostChangeLV.as_view(), name='change'),

    # Example: /board/1/modify/
    path('<int:pk>/modify/', views.post_modify, name='post_modify'),

    # Example: /board/1/delete/
    path('<int:pk>/delete/', views.post_delete, name='post_delete'),

    # Example: /board/category/
    path('category/', CategoryViewSet.as_view(), name='category_list'),

    # Example: /board/category/1/
    path('category/<int:id>/', CategorySearchViewSet.as_view(), name='post_in_category'),

    # Example: /board/near/list/
    path('near/list/', NearInfoListView.as_view(), name='post_near_list'),
]
