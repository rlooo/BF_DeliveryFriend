# <<<<<<< HEAD
#from django.contrib import admin
#
# # Register your models here.
# #=======
# from django.contrib import admin
#
# # Register your models here.
# #>>>>>>> 0a858dc2f8e9b3c2328155bb2472c4b3912bca34
#
from django.contrib import admin
from .models import Board

# 관리자(admin)가 게시글(Post)에 접근 가능
admin.site.register(Board)