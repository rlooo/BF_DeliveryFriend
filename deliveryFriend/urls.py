"""deliveryFriend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from login.views import KakaoSignInCallbackView, SignUpView
from board.views import *

# 이미지 업로드
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    #path('information/', views.information_list), # 기본 로그인 연습
    #path('information/<int:pk>/', views.information), # 기본 로그인 연습
    #path('auth/login/', views.login), # 기본 로그인 연습
    path('auth/kakao/login/', KakaoSignInCallbackView.as_view()),
    path('signup/', SignUpView.as_view()),
    path('board/list/', BoardListView.as_view()),
    #path('',index),
    #path('board/<int:pk>', posting, name="posting"),
    path('board/new_post/', new_post),
    path('chat/', include('chat.urls')),
    path('category/', CategoryViewSet.as_view()),
]

# 이미지 URL 설정
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)