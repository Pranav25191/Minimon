from django.db import models

# Create your models here.
class ChatRoom(models.Model):
    room_name = models.CharField(max_length=100)
    created_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


class ChatMessages(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    message = models.TextField()
    sender = models.CharField(max_length=100)    
    time = models.DateTimeField(auto_now_add=True)


