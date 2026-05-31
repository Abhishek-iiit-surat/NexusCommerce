from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Order, OrderItem


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
        read_only_fields = ['id', 'order']


class OrderSerializer(ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['id', 'user_id', 'status', 'total_amount', 'created_at', 'updated_at']


class CreateOrderSerializer(serializers.Serializer):
    shipping_address = serializers.JSONField()
    items = OrderItemSerializer(many=True)

class CreateOrderItemSerializer(serializers.Serializer):
      product_id = serializers.IntegerField()
      product_name = serializers.CharField(max_length=255)
      price_snapshot = serializers.DecimalField(max_digits=10,decimal_places=2)
      quantity = serializers.IntegerField(min_value=1)
