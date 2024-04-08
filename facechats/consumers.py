import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import FaceChat

class FaceChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id'] # URL 경로에서 방 ID를 추출합니다.
        self.room_group_name = 'chat_%s' % self.room_id

        if not await self.check_room_exists(self.room_id): # 방이 존재하는지 확인합니다.
                raise ValueError('채팅방이 존재하지 않습니다.')

        # Check if room exists and is not full
        room = await self.get_room(self.room_id)
        if not room or room.current_participants >= room.max_participants:
            await self.close()
            return
        
        # Increment participants count
        await self.increment_participants(room)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Decrement participants count
        await self.decrement_participants()

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def get_room(self, room_id):
        try:
            room = FaceChat.objects.get(pk=room_id)
            return room
        except FaceChat.DoesNotExist:
            return None

    @database_sync_to_async
    def increment_participants(self, room): # 현재 방의 참가자 수 증가
        room.current_participants += 1
        room.save()

    @database_sync_to_async
    def decrement_participants(self): # 현재 방의 참가자 수 감소
        room = FaceChat.objects.get(pk=self.room_id)
        room.current_participants = max(0, room.current_participants - 1)  # Ensure count never goes below 0
        room.save()
