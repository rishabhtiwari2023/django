# urls.py
from django.urls import path
from .views import audio_chat

urlpatterns = [
    path('audio/<str:room_name>/', audio_chat, name='audio_chat'),
]