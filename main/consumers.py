import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging

class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            "orders_group",
            self.channel_name
        )
        await self.accept()
        logging.info("Connection established")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "orders_group",
            self.channel_name
        )
        logging.info("Connection disconnected")

    async def send_order_update(self, event):
        await self.send(text_data=json.dumps({
            'order_id': event['order_id'],
            'status': event['status'],
            'user': event['user'],
            'fullname': event['fullname'],
            'phone_number': event['phone_number'],
            'total_price': event['total_price'],
            'order_items': event['order_items'],
        }))
        logging.info("Info sent")
