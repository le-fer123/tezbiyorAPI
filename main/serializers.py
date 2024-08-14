from rest_framework import serializers
from .models import User, Category, Product, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'desc', 'created_at', 'price', 'category', 'img')


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'desc', 'created_at', 'img', 'products')


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'product', 'price', 'quantity', 'status',)


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
        'id', 'user', 'shipping_address', 'total_price', 'status', 'desc', 'created_at', 'updated_at', 'order_items')


class UserSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('tg_id', 'fullname', 'phone_number', 'created_at', 'orders')
