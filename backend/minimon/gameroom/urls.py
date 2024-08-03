from django.urls import path
from .views import StartNewGame, JoinGame

urlpatterns = [
    path('new/', StartNewGame.as_view()),
    path('join/', JoinGame.as_view())
]
