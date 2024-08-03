import logging
import json
import uuid
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from faker import Faker
from wonderwords import RandomWord

from .handlers.game_session import create_game_token
from minimon.common.dto.response_dto import ResponseDTO
from gameroom.dto.create_game_token import CreateGameTokenDTO
from gameroom.models import GameRoom
from chatroom.models import ChatRoom


logger = logging.getLogger(__name__)

class StartNewGame(APIView):
	
    def post(self, request):
        try:
            # Code to start a new game
            data = request.data

            private_room_id = data.get("private_room_id")
            player_id = str(uuid.uuid4().hex)
            faker= Faker()
            player_name = data.get("player_name", faker.user_name())
            
            r = RandomWord()
            random_rn = r.random_words(include_parts_of_speech=["nouns", "adjectives"])[0] + \
                        r.random_words(include_parts_of_speech=["nouns", "adjectives"])[0]
            
            # Check if the Game Room exists
            game_room = GameRoom.objects.filter(game_room_code=private_room_id, is_active=True).exists()
            if game_room:
                return Response({
                    "status": False,
                    "error_code": "ERR-400",
                    "message": "Room already exists. Please join the room to start the game."
                }, status=status.HTTP_400_BAD_REQUEST)
            
            new_chat_room = ChatRoom.objects.create(
                # create random chat room name here for each new room using some text
                room_name = f"Room{random_rn}"
            )

            new_game_room = GameRoom.objects.create(
                game_room_name=data.get("game_room_name", f"Game{random_rn}"),
                game_room_code=private_room_id,
                chat_room_id= new_chat_room,
                players_uid={player_id:player_name},
                player_count=1,
                game_status="waiting",
                game_data={},
                is_active=True
            )

            create_game_token_dto = CreateGameTokenDTO(room_id=private_room_id, player_id=player_id, player_name=player_name)
            game_token : ResponseDTO = create_game_token(create_game_token_dto)
            if not game_token.status:
                return Response({
                    "status": False,
                    "error_code": "ERR-400",
                    "message": "Unable to start new game. Please try again later."
                }, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({
                "status": True,
                "data": game_token.data
            })
        except Exception as e:
            logger.error(f"Error while starting new game: {str(e)}")
            return Response({
                "status": False,
                "error_code" : "ERR-500",
                "mesaage": "Internal server error. Please try again later."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class JoinGame(APIView):
    def post(self, request):
        try:
            data = request.data

            private_room_id = data.get("private_room_id")
            player_id = str(uuid.uuid4().hex)
            player_name = data.get("player_name")

            # Check if the Game Room exists
            game_room = GameRoom.objects.filter(game_room_code=private_room_id, is_active=True)
            if not game_room.exists():
                return Response({
                    "status": False,
                    "error_code": "ERR-400",
                    "message": "Room does not exists. Please enter a valid room code."
                }, status=status.HTTP_400_BAD_REQUEST)
            
            create_game_token_dto = CreateGameTokenDTO(room_id=private_room_id, player_id=player_id, player_name=player_name)
            game_token : ResponseDTO = create_game_token(create_game_token_dto)
            if not game_token.status:
                return Response({
                    "status": False,
                    "error_code": "ERR-400",
                    "message": "Unable to join game. Please try again later."
                }, status=status.HTTP_400_BAD_REQUEST)
            
            
            game_room : GameRoom = game_room.first()
            if player_id in game_room.players_uid.keys():
                return Response({
                    "status": False,
                    "error_code": "ERR-400",
                    "message": "Player already exists in the room."
                }, status=status.HTTP_400_BAD_REQUEST)
            
            game_room.player_count += 1
            game_room.players_uid[player_id] = player_name
            game_room.save()

            return Response({
                "status": True,
                "data": game_token.data
            })
        except Exception as e:
            logger.error(f"Error while joining game: {str(e)}")
            return Response({
                "status": False,
                "error_code": "ERR-500",
                "message": "Internal server error. Please try again later."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    