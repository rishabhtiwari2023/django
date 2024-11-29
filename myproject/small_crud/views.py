# views.py
from django.shortcuts import render

def audio_chat(request, room_name):
    return render(request, 'audio_chat.html', {'room_name': room_name})