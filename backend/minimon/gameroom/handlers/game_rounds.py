import logging
from random import randint
from gameroom.models import GuessWords 

logger = logging.getLogger(__name__)

class GameRound:
    
    @classmethod
    def get_word(cls):
        # Get a random word from the database
        random_number = randint(1, 1000)
        return GuessWords.objects.get(id=random_number).word
    