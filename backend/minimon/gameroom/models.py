from django.db import models
from chatroom.models import ChatRoom

# Create your models here.

class GameRoom(models.Model):
    game_room_name = models.CharField(max_length=100, default="Minimon Game Room")
    game_room_code = models.CharField(max_length=60, primary_key=True)
    chat_room_id = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, null=True)
    players_uid = models.JSONField(default=dict)
    player_count = models.IntegerField(default=0)
    game_status = models.CharField(max_length=20, default="waiting")
    game_data = models.JSONField(default=dict)
    created_by = models.CharField(max_length=100,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

class GuessWords(models.Model):
    id = models.AutoField(primary_key=True)
    word = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    used_cnt = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    