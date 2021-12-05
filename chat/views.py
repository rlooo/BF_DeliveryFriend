import json
from datetime import datetime
from json import JSONEncoder

from django.core.serializers.json import DjangoJSONEncoder
from haikunator import Haikunator
from django.db import transaction
from rest_framework import generics

# Create your views here.
from django.shortcuts import render
from django.views import View

from . import models
from .models import Room, Message
from .serializer import *

from django.http import HttpResponse, JsonResponse

from django.forms.models import model_to_dict

class ProfileDetailView(View):
    def get(self, request, id):
        queryset = Account.objects.filter(social_login_id=id)
        serializer = AccountSerializer(queryset, many=True)
        return HttpResponse(json.dumps(serializer.data, ensure_ascii=False, indent='\t'), status=200)


# 랜덤으로 방 이름을 만듦
def new_room(request):
    new_room = None
    while not new_room:
        with transaction.atomic():
            haikunator = Haikunator()
            label = haikunator.haikunate() # 랜덤으로 label 만듦
            if Room.objects.filter(label=label).exists():
                continue
            new_room=Room.objects.create(label=label) # 생성한 label 값으로 새로운 방을 만듦
            new_room.save()

    data = json.loads(request.body)
    if Account.objects.filter(pk=data['author']).exists():
        author_info = Account.objects.get(pk=data['author'])
    social_login_id = author_info.social_login_id
    nickname = author_info.nickname
    profile_image = author_info.profile_image
    return JsonResponse({'label':label,
                         'social_login_id':social_login_id,
                         'nickname':nickname,
                         'profile_image':profile_image}, status=200)


def room(request, room_name):
    if request.method == 'POST':
        data = json.loads(request.body)

    if not Room.objects.filter(label=data['room_name']).exists():
        new_room=Room.objects.create(label=data['room_name']) # 받은 room_name 값으로 새로운 방을 만듦
        new_room.save()

    # 채팅방과 최근 메시지를 보여준다
    # label에 해당하는 채팅방이 없으면 자동으로 생성한다.
    room, created = Room.objects.get_or_create(label=data['room_name'])

    last_ten = Message.objects.filter(room=room.pk).order_by('-timestamp')[:10]

    print(last_ten[0].message)
    print(last_ten[1].message)
    last_ten_in_ascending_order = reversed(last_ten)
    return HttpResponse(last_ten_in_ascending_order, status=200)



