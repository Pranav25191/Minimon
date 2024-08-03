import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import  database_sync_to_async
from .models import ChatMessages, ChatRoom
from asgiref.sync import async_to_sync

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        
        self.chatroom_name = self.scope['url_route']['kwargs']['room_name']
        print("connected", self.channel_layer)
        print("connected", self.channel_name)
        print("connected", self.chatroom_name)

         # Join room group
        await self.channel_layer.group_add(
            self.chatroom_name,
            self.channel_name
        )

        await self.accept()
        await self.send(text_data = json.dumps({
            'message': "Welcome to the chat channel!"
        }))

        await self.channel_layer.group_send(
            self.chatroom_name,
            {
                'type': 'message',
                'message': f'A new user joined your channel! {self.channel_name}'
            }
        )
    
    async def disconnect(self, event):
        print("disconnected", self.channel_layer)
        print("disconnected", self.channel_name)
    
    async def receive(self, text_data):
        print("received", text_data)
        data = json.loads(text_data)
        print("received", data)
        await self.send(text_data=json.dumps({
            'message': data['access_token']
        }))
    
    async def chat_message(self, event):
        print("chat_message", event)
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))
    
    async def message(self, event):
        print("message", event)
        user = event.get('user', 'Anonymous')
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data = json.dumps(
            {
                'user': user,
                'message': message
            }
        ))
    
    # @database_sync_to_async
    # def get_chatroom(self, room_name):
    #     return chatroom.objects.get(room_name=room_name)
    
    @database_sync_to_async
    def get_chat_messages(self, room_name):
        
        chat_room =  ChatMessages.objects.filter(room_name=room_name).exists()
        if not chat_room:
            ChatRoom.objects.create(room_name=room_name, 
                                    creaed_by=self.channel_name)
        
        return
        
    @database_sync_to_async
    def create_chat_message(self, room_name, message):
        return ChatMessages.objects.create(room_name=room_name, message=message)
    
