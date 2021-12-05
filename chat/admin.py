from django.contrib import admin
from .models import Room
from .models import Message

admin.site.register(Room)

admin.site.register(Message)