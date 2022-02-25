#jwt 토큰 유효성 검사
# import ALGORITHM as ALGORITHM
import jwt
from django.http import JsonResponse

from deliveryFriend.my_settings import SECRET
from user.models import Account


def id_auth(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            payload = jwt.decode(access_token, SECRET, algorithms='HS256')
            user = Account.objects.get(id=payload("id"))

            return func(self, request, *args, **kwargs)

        except jwt.DecodeError:
            return JsonResponse({'MESSAGE': 'INVALID_TOKEN'}, status=401)

        except jwt.InvalidTokenError:
            return JsonResponse({'MESSAGE': 'INVALID_ACCESS_TOKEN'}, status=401)

        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'EXPIRED_TOKEN'}, status=401)

        except Account.DoesNotExist:
            return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)
