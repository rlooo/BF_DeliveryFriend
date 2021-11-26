from django.urls import path

from django.conf.urls import include, url
from . import views
from chat import views # 수정

urlpatterns = [
    path('', views.index, name='index'),
    #url(r'^$', views.about, name='about'), # 수정
    #url(r'^new/$', views.new_room, name='new_room'), # 수정
    path('<str:room_name>/', views.room, name='room'),
]