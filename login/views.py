import json
import bcrypt
import jwt
import requests

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
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
        print(data)
        return HttpResponse(status=201)

@method_decorator(csrf_exempt, name='dispatch')
class KakaoSignInCallbackView(View): # 카카오톡 소셜로그인을 위한 클래스
    # 백엔드에서는 프론트에서 받은 카카오의 사용자 토큰을 이용해 카카오에 사용자 정보를 요청한다.
    def get(self, request):
        kakao_access_code=request.GET.get("access_token",None)
        print(kakao_access_code)
        url="https://kapi.kakao.com/v2/user/me"
        headers={
            "Authorization":f"Bearer {kakao_access_code}",
            "Content-type":"application/x-www-form-urlencoded; charset=utf-8"
        }
        kakao_response=requests.post(url, headers=headers)
        kakao_response = json.loads(kakao_response.text) # 유저의 정보를 json화해서 변수에 저장

    # 관리자가(employee) 기존에 카카오톡 계정이 DB에 저장되어 있는지 확인
        if Account.objects.filter(social_login_id=kakao_response['id']).exists():  # 지금 접속한 카카오 아이디가 데이터베이스에 존재하는지 확인
            user_info = Account.objects.get(social_login_id=kakao_response['id'])  # 존재하는 카카오 아이디를 가진 유저 객체를 가져옴
            encoded_jwt = jwt.encode({'id': user_info.id}, SECRET_KEY, algorithm='HS256')  # jwt토큰 발행
            return HttpResponse(f'id:{user_info.id}, token:{encoded_jwt}, exist:true')

    # 저장되어 있지 않다면 코드 400 리턴
        else:
            user_info = Account(
                social_login_id=kakao_response['id'],
                email=kakao_response['kakao_account'].get('email',None),
            )
            user_info.save()
            # 일단 받아온 카카오 id와 email 저장, jwt 토큰은 프론트로 리턴해줄 필요가 없나?
            # 한 회원의 정보로 인식하기 위해서 social_login_id도 함께 리턴
            return HttpResponse(f'id:{user_info.id}', status=400)

@csrf_exempt
class SignUpView(View):
    def post(request):
        try:
            data = json.loads(request.body)

            if Account.objects.filter(social_login_id=data['id']).exists():
                user_info = Account.objects.get(social_login_id=data['id'])

            email=user_info.email
            user_info.profile_image = data['image']
            user_info.nickname = data['nickname']

            if Account.objects.filter(nickname=user_info.nickname).exist():
                return JsonResponse({'message' : 'ALREADY_EXITSTS'}, status=400)

            return JsonResponse({
                'id': user_info.social_login_id,
                'email': user_info.email,
                'nickname':user_info.nickname,
                'image':user_info.profile_image,
            }, status=201)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)