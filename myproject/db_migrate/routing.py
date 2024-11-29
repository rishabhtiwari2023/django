# db_migrate/routing.py
from django.urls import path
from .consumers import ItemConsumer

websocket_urlpatterns = [
    path('ws/items/', ItemConsumer.as_asgi()),
]