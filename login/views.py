import json
import bcrypt
import jwt
import requests

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Information
from .serializers import InformationSerializer
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from django.shortcuts import redirect
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from .models import Account

from deliveryFriend.settings import KAKAO_KEY, SECRET_KEY

# Create your views here.

@csrf_exempt
def information_list(request):
    if request.method == 'GET':
        query_set = Information.objects.all()
        serializer = InformationSerializer(query_set, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method =='POST':
        data = JSONParser().parse(request)
        serializer = InformationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def information(request, pk):

    obj = Information.objects.get(pk=pk)

    if request.method == 'GET':
        serializer = InformationSerializer(obj)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = InformationSerializer(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        obj.delete()
        return HttpResponse(status=204)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        search_name = data['name']
        obj = Information.objects.get(name=search_name)
        print(obj.phone_number)

        if data['phone_number'] == obj.phone_number:
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)

class KakaoSignInCallbackView(View): # 카카오톡 소셜로그인을 위한 클래스
    # 백엔드에서는 프론트에서 받은 카카오의 사용자 토큰을 이용해 카카오에 사용자 정보를 요청한다.
    def get(self, request):
        print("성공")
        access_token = request.headers["Authorization"]
        headers = ({'Authorization' : f"Bearer {access_token}"})
        url = "https://kapi.kakao.com/v1/user/me"  # Authorization(프론트에서 받은 토큰)을 이용해서 회원의 정보를 확인하기 위한 카카오 API 주소
        response = requests.request("POST", url, headers=headers) # API를 요청하여 회원의 정보를 response에 저장
        user = response.json() # 유저의 정보를 json화해서 변수에 저장

        # 관리자가(employee) 기존에 카카오톡 계정이 DB에 저장되어 있는지 확인
        if Account.objects.filter(social_login_id=user['sub']).exists(): # 지금 접속한 카카오 아이디가 데이터베이스에 존재하는지 확인
            user_info = Account.objects.get(social_login_id = user['sub']) # 존재하는 카카오 아이디를 가진 유저 객체를 가져옴
            encoded_jwt = jwt.encode({'id' : user_info.id}, SECRET_KEY, algorithm='HS256') # jwt토큰 발행

            return JsonResponse({ #jwt토큰, 이름, 타입 프론트엔드에 전달
                'access_token' : encoded_jwt.decode('UTF-8'),
                'user_name' : user_info.name,
                'user_pk' : user_info.id
            }, status=200) # 발행한 토큰을 응답

        # 저장되어 있지 않다면 DB에 저장
        else:
            new_user_info = Account(
                social_login_id=user['id'],
                name=user['properties']['nickname'],
                email=user['properties'].get('email', None) # 이메일 선택동의여서 없을 수도 있음
            )
            new_user_info.save() #db에 저장
            encoded_jwt = jwt.encode({'id': new_user_info.id}, SECRET_KEY, algorithm='HS256') # jwt토큰 발행

            return JsonResponse({ # DB에 저장된 회원의 정보를 access token과 같이 프론트엔드에게 전달
                'access_token': encoded_jwt.decode('UTF-8'),
                'user_name': new_user_info.name,
                'user_pk': new_user_info.id,
            }, status=200)
