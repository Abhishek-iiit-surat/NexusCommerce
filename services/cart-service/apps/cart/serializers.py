from rest_framework.serializers import ModelSerializer
from .models import Cart, CartItem

class CartItemSerializer(ModelSerializer):

    class Meta:
        model = CartItem
        fields = '__all__'
        read_only_fields = ['id','created_at', 'updated_at']


class CartSerializer(ModelSerializer):

    items = CartItemSerializer(many = True, read_only = True)

    class Meta:
        model = Cart
        fields = '__all__'
        read_only_fields = ['id','user_id']




