# # your_new_app/consumers.py

# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = 'chat_room'
#         self.room_group_name = 'chat_%s' % self.room_name

#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         username = text_data_json['username']
#         message = text_data_json['message']

#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'username': username,
#                 'message': message
#             }
#         )

#     async def chat_message(self, event):
#         username = event['username']
#         message = event['message']

#         await self.send(text_data=json.dumps({
#             'username': username,
#             'message': message
#         }))
# consumers.py
# consumers.py
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import authenticate
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("self.scope",self.scope)
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name# we can manuplate the group room name
        print("self.room_group_name",self.room_group_name)
        # Join room group
        # await self.channel_layer.group_add(
        #     self.room_group_name,
        #     self.channel_name # This is the unique channel name assigned by Channels
        # )

        # await self.accept()
        # if self.scope["user"].is_authenticated:#self.scope["user"] is the Django user object and self.scope["user"].is_authenticated is True if the user is logged in.
               # Extract user credentials from query string
        query_string = self.scope['query_string'].decode()
        query_params = dict(param.split('=') for param in query_string.split('&'))
        username = query_params.get('username')
        password = query_params.get('password')
     # Authenticate user
        user = await self.authenticate_user(username, password)
        if user is not None:
            self.scope['user'] = user
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    @database_sync_to_async
    def authenticate_user(self, username, password):
        from django.contrib.auth import authenticate
        return authenticate(username=username, password=password)

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope['user']
        await self.save_message(user, self.room_name, message)
        print("-----------------self.channel_layer",self.channel_layer)
        print("-----------------self.room_group_name",self.room_group_name)
        # Send message to room group
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_channel_name': self.channel_name
            }
        )
    @database_sync_to_async
    def save_message(self, user, room_name, message):
        from .models import Message
        Message.objects.create(user=user, room_name=room_name, content=message)
       
    async def chat_message(self, event):
        message = event['message']
        print("########################event",event)
        sender_channel_name = event['sender_channel_name']

        # Send message to WebSocket only if it's not the sender
        if self.channel_name != sender_channel_name:
            await self.send(text_data=json.dumps({
                'message': message
            }))



# Client Sends Message: When a user sends a message from the frontend,
#     it is sent to the server via WebSocket.
# Server Receives Message: The server (Django Channels consumer) receives this message.
# Broadcast to Group: The server then broadcasts this message to all clients in the same chat room group.
# Check Sender: When broadcasting, the server includes the sender's channel name.
# Filter Message: Each client checks if the message is from their own channel.
# Display Message: If the message is not from their own channel, the client displays it. 
#     This prevents the sender from seeing their own message twice.

# Create a Room: One person (let’s call them Person A) creates a new chat room or group in the app.

# Invite the Other Person: Person A then sends an invite to the second person (Person B) to join the room. 
#        This could be done by sharing a link or by selecting Person B from a contact list.

# Room ID: The app will generate a unique "room ID" or link for the chat room, 
#               which both people use to enter the conversation.

# Start Chatting: Once Person B accepts the invite and enters the room, both people can start chatting in that room.

# So, in short:

# Person A creates a room.
# Person B joins with a room ID or invite link.
# Both can chat in that room.


# self.scope {'type': 'websocket', 'path': '/ws/chat/1/', 'raw_path': b'/ws/chat/1/', 
# 'root_path': '', 'headers': [(b'host', b'127.0.0.1:8000'), (b'connection', b'Upgrade'), 
# (b'pragma', b'no-cache'), (b'cache-control', b'no-cache'), (b'user-agent', b'Mozilla/5.0 
# (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'), 
# (b'upgrade', b'websocket'), (b'origin', b'http://127.0.0.1:8000'), (b'sec-websocket-version', b'13')
# , (b'accept-encoding', b'gzip, deflate, br, zstd'), (b'accept-language', b'en-GB,en;q=0.9'), 
# (b'sec-websocket-key', b'FOdH9mJHlaCU4qk/7pMICA=='), (b'sec-websocket-extensions', 
# b'permessage-deflate; client_max_window_bits')], 'query_string': b'', 'client': ['127.0.0.1', 33890]
# , 'server': ['127.0.0.1', 8000], 'subprotocols': [], 'asgi': {'version': '3.0'}, 'cookies': {}, 
# 'session': <django.utils.functional.LazyObject object at 0x7fbcb0b508b0>, 'user': <channels.auth.UserLazyObject object at 0x7fbcb0b514e0>,
#  'path_remaining': '', 'url_route': {'args': (), 'kwargs': {'room_name': '1'}}}
# self.room_group_name chat_1
# daphne -p 8000 myproject.asgi:application