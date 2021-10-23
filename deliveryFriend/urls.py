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
from login import views
from login.views import KakaoSignInCallbackView
from login.views import SignUpView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('information/', views.information_list), # 기본 로그인 연습
    path('information/<int:pk>/', views.information), # 기본 로그인 연습
    path('auth/login/', views.login), # 기본 로그인 연습
    path('auth/kakao/login/', views.KakaoSignInCallbackView.as_view()),
    path('signup/', views.SignUpView),
    #path('categoryCreate/', views.categoryCreate, name = 'categoryCreate'),
]
