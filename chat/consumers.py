import json
import logging

import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Room, Message
log = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room = self.scope['url_route']['kwargs']['label'] # label은 채팅룸의 라벨 속성에 매핑
        self.room_group_name = 'chat_%s' % self.room

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept() # 웹소켓 연결 승낙

    # Receive message from WebSocket
    # 해당 웹소켓에 메시지가 수신될 때마다 consumer가 호출된다
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']  # json 메시지 파싱

        # Send message to room group
        await self.channel_layer.group_send( # 그룹에 들어감
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

# @channel_session # 웹소켓 연결이 매핑된 룸이 어떤 룸인지 기억하는 방식
# def ws_connect(message):
#     try: # 클라이언트는 /chat/{label}/ 형식의 URL을 통해 웹소켓에 연결된다
#         prefix, label = message['path'].strip('/').split('/') # Consumer는 message['path']를 통해 웹소켓 경로를 파싱한다
#         if prefix!='chat':
#             log.debug('invalid ws path=%s', message['path'])
#             return
#         room = Room.objects.get(label=label) # label은 채팅룸의 라벨 속성에 매핑
#     except ValueError:
#         log.debug("invalid ws path=%s", message['path'])
#         return
#     except Room.DoesNotExitst:
#         log.debug('ws room does not exist label=%s', label)
#         return
#
#     log.debug('chat connect room=%s client=%s:%s path=%s reply_channel=%s',
#               room.label, message['client'][0], message['client'][1], message['path'], message.reply_channel)
#
#     message.reply_channel.send({"accept":True})
#     Group('chat-'+label, channel_layer=message.channel_layer).add(message.reply_channel) # 메시지는 reply_channel 속성을 통해서 메시지를 클라이언트에게 다시 보낸다
#     # 그룹: 해당 메시지가 브로드캐스팅될 채널들의 연결, 해당 채팅룸에 특정된 그룹에 메시지의 reply_channel을 추가해야 함
#     message.channel_session['room']=room.label
#     # 클라이언트 연결 완료


# @channel_session
# def ws_receive(message):
#     try: # 해당 웹소켓에 메시지가 수신될 때마다 consumer가 호출된다
#         label = message.channel_session['room'] # channel_session에서 room을 추출
#         room = Room.obects.get(label=label) # 데이터베이스에서 해당 room을 찾음
#         log.debug('recieved message, room exist label=%s', room.label)
#
#     except KeyError:
#         log.debug('no room in channel_session')
#         return
#     except Room.DoesNotExist:
#         log.debug('recieved message, buy room does not exist label=%s', label)
#         return
#
#     try:
#         data = json.loads(message['text']) # json 메시지 파싱
#     except ValueError:
#         log.debug("ws message isn't json text=%s", data)
#         return
#
#     if set(data.keys()) != set(('handle', 'message')):
#         log.debug("ws message unexpected format data=%s", data)
#         return
#
#     if data:
#         log.debug('chat message room=%s handle=%s message=%s',
#                   room.label, data['handle'], data['message'])
#         m = room.messages.create(**data)
#
#         Group('chat-' + label, channel_layer=message.channel_layer).send({'text': json.dumps(m.as_dict())})
#         # 새로운 메시지를 채팅룸에 있는 모든 이들에게 브로드캐스팅
#         # Group.send()는 그룹에 추가된 모든 reply_channel에 이 메시지를 보낸다
#
# @channel_session
# def ws_disconnect(message):
#     try:
#         label = message.channel_session['room']
#         room = Room.objects.get(label=label)
#         Group('chat-' + label, channel_layer=message.channel_layer).discard(message.reply_channel)
#     except (KeyError, Room.DoesNotExist):
#         pass