from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import OrderItem, Order, Product
import logging
from django.db import transaction


@receiver(post_save, sender=OrderItem)
def update_order_total_on_save(sender, instance, **kwargs):
    if instance.order:
        instance.order.update_total_price()


@receiver(post_delete, sender=OrderItem)
def update_order_total_on_delete(sender, instance, **kwargs):
    if instance.order:
        instance.order.update_total_price()


@receiver(post_save, sender=Product)
def update_order_item(sender, instance, **kwargs):
    order_items = OrderItem.objects.filter(product=instance)
    for order_item in order_items:
        order_item.update_price()


@receiver(post_delete, sender=Product)
def delete_order_item(sender, instance, **kwargs):
    order_items = OrderItem.objects.filter(product=None)
    for order_item in order_items:
        order_item.delete_item_by_status()


@receiver(post_save, sender=Order)
def order_status_update(sender, instance, **kwargs):
    if kwargs.get('created', False):
        return
    logging.info(f"Order update sent: {instance.id}")
    if instance.status == 'ACTIVE':
        channel_layer = get_channel_layer()
        order_items = []
        items = instance.order_items.all()

        for item in items:
            if item.product is not None:
                order_items.append({
                    'item_id': item.id,
                    'product_name': item.product.name,
                    'price': str(item.price),
                    'quantity': item.quantity,
                })

        async_to_sync(channel_layer.group_send)(
            "orders_group",
            {
                "type": "send_order_update",
                "order_id": instance.id,
                "user": instance.user.tg_id,
                "fullname": instance.user.fullname,
                "phone_number": instance.user.phone_number,
                "status": instance.status,
                "total_price": str(instance.total_price),
                "order_items": order_items
            }
        )
        logging.info(f"Order update sent: {instance.id}")
