from django.urls import path

from django.conf.urls import include, url
from . import views

urlpatterns = [
    path('new_room/', views.new_room, name='new_room'),
    url(r'^(?P<label>[\w-]{,50})/$', views.chat_room, name='chat_room'),
]