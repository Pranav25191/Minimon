import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import  database_sync_to_async
from .models import GameRoom, ChatRoom
from asgiref.sync import async_to_sync
from .handlers.game_session import create_game_token, get_token_payload
from handlers.game_rounds import GameRound

class GameRoomConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        
        self.chatroom_name = self.scope['url_route']['kwargs']['room_name']
        print("connected", self.channel_layer)
        print("connected", self.channel_name)
        print("connected", self.chatroom_name)

        token_data = self.scope.get('token_data')
        game_room_id = token_data.get('room_id')

        # Join room group
        await self.channel_layer.group_add(
            game_room_id,
            self.channel_name
        )

        await self.accept()
        player_list = await self.get_player_list(game_room_id)        
        await self.send(text_data = json.dumps({
            'message': f"Hi {token_data.get('player_name')}, Welcome to the chat channel!",
            'player_list' : player_list
        }))

        await self.channel_layer.group_send(
            game_room_id,
            {
                'type': 'message',
                'message': f'A new played joined',
                'player_name' : token_data.get('player_name')
            }
        )
    
    async def disconnect(self, event):
        print("disconnected", self.channel_layer)
        print("disconnected", self.channel_name)
    
    async def receive(self, text_data):
        print("received", text_data)
        print("self person", self.channel_name, self.channel_layer)
        token_data =  self.scope['token_data']
        print("received", token_data)

        await self.channel_layer
        
        await self.send(text_data=json.dumps({
            'message': GameRound.get_word()
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
    def create_or_update_gameroom(self, room_name):
        
        game_room =  GameRoom.objects.filter(room_name=room_name).exists()
        if not game_room:
            ChatRoom.objects.create(room_name=room_name,
                                    created_by=self.channel)
            GameRoom.objects.create(
                game_room_code=room_name,



            )
        
        return
        
    @database_sync_to_async
    def get_player_list(self, room_id):
        game_room = GameRoom.objects.get(game_room_code=room_id)
        return list(game_room.players_uid.values())
    
