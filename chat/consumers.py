import json
import logging

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        senderId = text_data_json['senderId']
        receiverId = text_data_json['receiverId']

        room = await self.get_room() # 데베 저장
        new_message = await self.get_new_message(room, senderId, receiverId, message) # 데베 저장

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'senderId' : senderId,
                'receiverId' : receiverId,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        senderId = event['senderId']
        receiverId = event['receiverId']


        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'senderId' : senderId,
            'receiverId' : receiverId
        }))

    @database_sync_to_async
    def get_room(self):
        return Room.objects.get(label=self.room_name)

    @database_sync_to_async
    def get_new_message(self, room, senderId, receiverId, message):
        new_message = Message.objects.create(
            room=room,
            senderId=senderId,
            receiverId=receiverId,
            message=message,
        )
        new_message.save()
        return new_message