from django.urls import path

from user.views import *

app_name = 'user'
urlpatterns = [
    # Example: /user/auth/kakao/
    path('auth/kakao/', KakaoSignInCallbackView.as_view(), name='auth_kakao'),

    # Example: /user/signup/
    path('signup/', SignUpView.as_view(), name='signup'),

    # Example: /user/delete/
    path('delete/', user_delete, name='user_delete'),

    # Example: /user/location/
    path('location/', set_location, name='set_location'),
]
