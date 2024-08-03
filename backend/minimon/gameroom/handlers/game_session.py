import jwt
import logging

from minimon.settings import SECRET_KEY
from gameroom.dto.create_game_token import CreateGameTokenDTO
from minimon.common.dto.response_dto import ResponseDTO

logger = logging.getLogger(__name__)

def create_game_token(create_game_dto: CreateGameTokenDTO) -> ResponseDTO:
    try:
        logger.info(f"Creating game token for room_id: {create_game_dto.room_id} and player_id: {create_game_dto.player_id}")
        payload = {
            "room_id": create_game_dto.room_id,
            "player_id": create_game_dto.player_id,
            "player_name": create_game_dto.player_name
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return ResponseDTO(status=True, data={
                "game_token": token
            })
    except Exception as e:
        logger.error(f"Error while creating game token: {str(e)}")
        return ResponseDTO(status=False, message="Internal server error. Please try again later.")

def get_token_payload(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return {
            "error": "Token has expired"
        }
    except jwt.InvalidTokenError:
        return {
            "error": "Invalid token"
        }
    except Exception as e:
        return {
            "error": str(e)
        }