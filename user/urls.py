from django.urls import path

from user.views import *

app_name = 'user'
urlpatterns = [
    # Example: /user/auth/kakao/
    path('auth/kakao/', KakaoSignInCallbackView.as_view(), name='auth_kakao'),

    # Example: /user/signup/
    path('signup/', SignUpView.as_view(), name='signup'),
]
