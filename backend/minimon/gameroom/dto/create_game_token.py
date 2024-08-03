from .base_dto import BaseDTO


class CreateGameTokenDTO(BaseDTO):

    def __init__(self, room_id: int, player_id: int, **kwargs):
        self.room_id = room_id
        self.player_id = player_id
        self.player_name = kwargs.get('player_name', None)
        self.__dict__.update(kwargs)