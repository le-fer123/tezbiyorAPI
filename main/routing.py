from django.urls import path
from .consumers import OrderConsumer

ws_urlpatterns = [
    path('ws/orders/', OrderConsumer.as_asgi()),
]
