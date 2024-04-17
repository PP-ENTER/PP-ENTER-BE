import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import FaceChat
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

# class FaceChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_id = self.scope['url_route']['kwargs']['room_id'] # URL 경로에서 방 ID를 추출합니다.
#         self.room_group_name = 'chat_%s' % self.room_id

#         if not await self.check_room_exists(self.room_id): # 방이 존재하는지 확인합니다.
#                 raise ValueError('채팅방이 존재하지 않습니다.')

#         # Check if room exists and is not full
#         room = await self.get_room(self.room_id)
#         if not room or room.current_participants >= room.max_participants:
#             await self.close()
#             return

#         # Increment participants count
#         await self.increment_participants(room)

#         # Join room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         # Decrement participants count
#         await self.decrement_participants()

#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )

#     # Receive message from room group
#     async def chat_message(self, event):
#         message = event['message']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))

#     @database_sync_to_async
#     def get_room(self, room_id):
#         try:
#             room = FaceChat.objects.get(pk=room_id)
#             return room
#         except FaceChat.DoesNotExist:
#             return None

#     @database_sync_to_async
#     def increment_participants(self, room): # 현재 방의 참가자 수 증가
#         room.current_participants += 1
#         room.save()

#     @database_sync_to_async
#     def decrement_participants(self): # 현재 방의 참가자 수 감소
#         room = FaceChat.objects.get(pk=self.room_id)
#         room.current_participants = max(0, room.current_participants - 1)  # Ensure count never goes below 0
#         room.save()


class CallConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        # response to client, that we are connected.
        self.send(
            text_data=json.dumps(
                {"type": "connection", "data": {"message": "Connected"}}
            )
        )

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(self.my_name, self.channel_name)

    # Receive message from client WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # print(text_data_json)

        eventType = text_data_json["type"]

        if eventType == "login":
            name = text_data_json["data"]["name"]

            # we will use this as room name as well
            self.my_name = name

            # Join room
            async_to_sync(self.channel_layer.group_add)(self.my_name, self.channel_name)

        if eventType == "call":
            name = text_data_json["data"]["name"]
            print(self.my_name, "is calling", name)
            # print(text_data_json)

            # to notify the callee we sent an event to the group name
            # and their's groun name is the name
            async_to_sync(self.channel_layer.group_send)(
                name,
                {
                    "type": "call_received",
                    "data": {
                        "caller": self.my_name,
                        "rtcMessage": text_data_json["data"]["rtcMessage"],
                    },
                },
            )

        if eventType == "answer_call":
            # has received call from someone now notify the calling user
            # we can notify to the group with the caller name

            caller = text_data_json["data"]["caller"]
            # print(self.my_name, "is answering", caller, "calls.")

            async_to_sync(self.channel_layer.group_send)(
                caller,
                {
                    "type": "call_answered",
                    "data": {"rtcMessage": text_data_json["data"]["rtcMessage"]},
                },
            )

        if eventType == "ICEcandidate":

            user = text_data_json["data"]["user"]

            async_to_sync(self.channel_layer.group_send)(
                user,
                {
                    "type": "ICEcandidate",
                    "data": {"rtcMessage": text_data_json["data"]["rtcMessage"]},
                },
            )

    def call_received(self, event):

        # print(event)
        print("Call received by ", self.my_name)
        self.send(
            text_data=json.dumps({"type": "call_received", "data": event["data"]})
        )

    def call_answered(self, event):

        # print(event)
        print(self.my_name, "'s call answered")
        self.send(
            text_data=json.dumps({"type": "call_answered", "data": event["data"]})
        )

    def ICEcandidate(self, event):
        self.send(text_data=json.dumps({"type": "ICEcandidate", "data": event["data"]}))


# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_group_name = 'chat_room'

#         # Join room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         if data['type'] == 'invite':
#             # Process invite
#             await self.channel_layer.group_send(
#                 self.room_group_name,
#                 {
#                     'type': 'chat_invite',
#                     'room_id': data['room_id'],
#                     'invitee': data['invitee'],
#                     'inviter': data['inviter']
#                 }
#             )

#     # Handler for invite messages
#     async def chat_invite(self, event):
#         await self.send(text_data=json.dumps({
#             'type': 'invite',
#             'room_id': event['room_id'],
#             'invitee': event['invitee'],
#             'inviter': event['inviter']
#         }))


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    async def chat_message(self, event):
        message = event["message"]

        await self.send(text_data=json.dumps({"message": message}))
