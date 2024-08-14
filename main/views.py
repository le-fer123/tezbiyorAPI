from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import User, Category, Product, Order, OrderItem
from .serializers import UserSerializer, CategorySerializer, ProductSerializer, OrderSerializer, OrderItemSerializer


def index(request):
    return render(request, 'main/index.html')


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


def check_active_orders(request):
    orders = Order.objects.filter(status="ACTIVE").select_related('user').prefetch_related('order_items__product')
    orders_dir = {}
    for order in orders:
        orders_dir[order.id] = {
            "order_id": order.id,
            "status": order.status,
            "user": order.user.tg_id,
            "order.fullname": order.user.fullname,
            "order.phone_number": order.user.phone_number,
            "order.total_price": order.total_price,
            "order_items": {}
        }

        for item in order.order_items.all():
            if item.product:
                orders_dir[order.id]["order_items"][str(item.id)] = {
                    "order_item_id": item.id,
                    "product_name": item.product.name,
                    "price": item.price,
                    "quantity": item.quantity,
                }

    return JsonResponse(orders_dir)
