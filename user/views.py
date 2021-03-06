import json
import bcrypt
import jwt
import requests

from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.views import View

from .models import Account

from deliveryFriend.settings import KAKAO_KEY, SECRET_KEY


@method_decorator(csrf_exempt, name='dispatch')
class KakaoSignInCallbackView(View):  # 카카오톡 소셜로그인을 위한 클래스
    # 백엔드에서는 프론트에서 받은 카카오의 사용자 토큰을 이용해 카카오에 사용자 정보를 요청한다.
    def get(self, request):
        kakao_access_code = request.GET.get("access_token", None)

        url = "https://kapi.kakao.com/v2/user/me" # 사용자 정보를 가져오는 API 엔드포인트
        kakao_header = {
            "Authorization": f"Bearer {kakao_access_code}",
            "Content-type": "application/x-www-form-urlencoded; charset=utf-8"
        }
        kakao_response = requests.post(url, headers=kakao_header)
        data=json.loads(kakao_response.text)  # 유저의 정보를 json화해서 변수에 저장

        # 관리자가(employee) 기존에 카카오톡 계정이 DB에 저장되어 있는지 확인
        if Account.objects.filter(social_login_id=data['id']).exists():  # 지금 접속한 카카오 아이디가 데이터베이스에 존재하는지 확인
            user_info = Account.objects.get(social_login_id=data['id'])  # 존재하는 카카오 아이디를 가진 유저 객체를 가져옴
            encoded_jwt = jwt.encode({'id': user_info.id}, SECRET_KEY, algorithm='HS256')  # jwt 토큰 발행

            return JsonResponse({
                'id': user_info.social_login_id,
                'email': user_info.email,
                'nickname': user_info.nickname,
                'image': user_info.profile_image,
                'token': encoded_jwt,
            }, status=201)

        # 저장되어 있지 않다면 코드 400 리턴
        else:
            user_info = Account(
                social_login_id=data['id'],
                email=data['kakao_account'].get('email', None),
            )
            user_info.save()

            return JsonResponse({'id': user_info.social_login_id}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if Account.objects.filter(social_login_id=data['id']).exists():
                user_info = Account.objects.get(social_login_id=data['id'])

            user_info.nickname = data['nickname']
            user_info.profile_image = data['image']

            user_info.save()
            # if Account.objects.filter(nickname=user_info.nickname).exist():
            # return JsonResponse({'message' : 'ALREADY_EXITSTS'}, status=400)

            encoded_jwt = jwt.encode({'id': user_info.id}, SECRET_KEY, algorithm='HS256')  # jwt토큰 발행

            return JsonResponse({
                'id': user_info.social_login_id,
                'email': user_info.email,
                'nickname': user_info.nickname,
                'image': user_info.profile_image,
                'token': encoded_jwt,
            }, status=201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

def set_location(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        if Account.objects.filter(social_login_id=data['id']).exists():
            user_info = Account.objects.get(social_login_id=data['id'])

        user_info.longitude = float(data['longitude'])
        user_info.latitude = float(data['latitude'])

        user_info.save()

        return HttpResponse(status=200)

# 유저 삭제 기능
def user_delete(request):
    data = json.loads(request.body)
    user = Account.objects.get(email= data['email'])
    user.delete()
    return HttpResponse(status=200)