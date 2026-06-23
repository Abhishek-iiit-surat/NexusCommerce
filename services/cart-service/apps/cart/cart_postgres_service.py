from .models import Cart, CartItem
from .exceptions import CartNotFoundError, CartItemNotFoundError, InvalidQuantityError
from .cart_redis_service import CartRedisService
from django.db import transaction

class CartPostgresService:

    def __init__(self):
        self.cart_redis_service = CartRedisService()

    def flush_cart(self, user_id, items):
        """
        get the existing cart of the user if exists, else create 
        a new cart and then clear the cart then flush new items
        to the cart and unmark dirty on the redis cart
        """
        cart, _ = Cart.objects.get_or_create(user_id=user_id)

        with transaction.atomic():
            CartItem.objects.filter(cart=cart).delete()
            cart_items = [
                CartItem(
                    cart=cart,
                    product_id=item["product_id"],
                    quantity=item["quantity"]
                )
                for item in items
            ]
            CartItem.objects.bulk_create(cart_items)
            self.cart_redis_service.clear_dirty(user_id)

        