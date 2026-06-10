from rest_framework import serializers


class AddCartItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1)


class UpdateCartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)


class CartItemResponseSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    added_at = serializers.CharField()


class CartResponseSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    items = CartItemResponseSerializer(many=True)
