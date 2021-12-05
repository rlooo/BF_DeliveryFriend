from django.urls import path

from django.conf.urls import include, url
from . import views
from chat import views # 수정

urlpatterns = [
    #url(r'^$', views.about, name='about'), # 수정
    #url(r'^new/$', views.new_room, name='new_room'), # 수정
    path('room/<str:room_name>/', views.room),
    path('new_room/', views.new_room),
]