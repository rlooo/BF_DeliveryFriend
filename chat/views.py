import json

from haikunator import Haikunator
from django.db import transaction
from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render
from django.views import View

from .models import Room,Message
from .serializer import *

from django.http import HttpResponse, JsonResponse

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
    if Account.objects.filter(social_login_id=data['author']).exists():
        author_info = Account.objects.get(social_login_id=data['author'])

    return JsonResponse({'label':label, 'author_info':author_info}, status=200)
#
# 실제 채팅이 이루어짐
# def chat_room(request, room_name):
#     # 채팅방과 최근 메시지를 보여준다
#
#     # label에 해당하는 채팅방이 없으면 자동으로 생성한다.
#     room, created = Room.objects.get_or_create(label=room_name)
#     # 가장 최근 50개의 메시지 보여줌
#     messages = reversed(room.messages.order_by('-timestamp'[:50]))
#
#     return render(request, "chat/room.html", {
#         'room_name':room_name,
#         'room': room,
#         'messages': messages,
#     })
#     # return HttpResponse(room, messages, status=200)

def index(request):
    return render(request, 'chat/index.html', {})

def room(request, room_name):
    if request.method == 'POST':
        data = json.loads(request.body)

    if not Room.objects.filter(label=data['room_name']).exists():
        new_room=Room.objects.create(label=data['room_name']) # 받은 room_name 값으로 새로운 방을 만듦
        new_room.save()

    # 채팅방과 최근 메시지를 보여준다
    # label에 해당하는 채팅방이 없으면 자동으로 생성한다.
    room, created = Room.objects.get_or_create(label=['room_name'])
    # 가장 최근 50개의 메시지 보여줌
    messages = reversed(room.messages.order_by('-timestamp'[:50]))

    return JsonResponse({'messages' :messages}, status=200)