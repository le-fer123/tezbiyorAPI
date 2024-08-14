from decimal import Decimal
from channels.layers import get_channel_layer
from channels.testing import WebsocketCommunicator
from django.test import TestCase
from project.asgi import application
from main.models import *

class WebSocketTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            tg_id=12345,
            fullname='John Doe',
            phone_number='1234567890'
        )

        self.category = Category.objects.create(
            name='Electronics',
            desc='Electronic gadgets and devices',
            img='path/to/category/image.jpg'
        )

        self.product = Product.objects.create(
            name='Smartphone',
            desc='Latest model smartphone',
            price=Decimal('299.99'),
            category=self.category,
            img='path/to/product/image.jpg'
        )

        self.order = Order.objects.create(
            user=self.user,
            shipping_address='123 Test Street',
            total_price=Decimal('299.99'),
            status='Pending',
            desc='Test order'
        )

        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=Decimal('299.99'),
            quantity=1
        )

    async def test_websocket_connection(self):
        communicator = WebsocketCommunicator(application, "/ws/orders/")
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            "orders_group",
            {
                "type": "send_order_update",
                "order_id": self.order.id,
                "status": self.order.status,
                "user": self.user.tg_id,
                "fullname": self.user.fullname,
                "phone_number": self.user.phone_number,
                "total_price": str(self.order.total_price),
                "order_items": [
                    {
                        "product_name": self.product.name,
                        "quantity": self.order_item.quantity,
                        "price": str(self.order_item.price)
                    }
                ]
            }
        )

        response = await communicator.receive_json_from()
        print(response)
        self.assertEqual(response['order_id'], self.order.id)
        self.assertEqual(response['status'], self.order.status)
        self.assertEqual(response['user'], self.user.tg_id)
        self.assertEqual(response['fullname'], self.user.fullname)
        self.assertEqual(response['phone_number'], self.user.phone_number)
        self.assertEqual(response['total_price'], str(self.order.total_price))
        self.assertEqual(response['order_items'][0]['product_name'], self.product.name)
        self.assertEqual(response['order_items'][0]['quantity'], self.order_item.quantity)
        self.assertEqual(response['order_items'][0]['price'], str(self.order_item.price))

        await communicator.disconnect()
