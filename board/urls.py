from django.urls import path

from board import views
from board.views import *

app_name = 'board'
urlpatterns = [

    # Example: /board/search
    path('search/', views.SearchView.as_view(), name='search'),

    # Example: /board/new_post/
    path('new_post/', new_post, name='new_post'),

    # Example: /board/list/
    path('list/', BoardListView.as_view(), name='list'),

    # Example: /board/change/
    #path('change/', views.PostChangeLV.as_view(), name='change'),

    # Example: /board/1/update/
    #path('<int:pk>/update/', views.PostUpdateView.as_view(), name='update'),

    # Example: /board/1/delete/
    #path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='delete'),

    # Example: /board/category
    path('category/', CategoryViewSet.as_view()),

    # Example: /board/category/1
    path('category/<int:id>/', CategorySearchViewSet.as_view()),
]
