from .models import Cart, CartItem
from .exceptions import CartNotFoundError, CartItemNotFoundError, InvalidQuantityError
from .cart_redis_service import CartRedisService

class CartPostgresService:

    def __init__(self):
        self.cart_redis_service = CartRedisService()

    def flush_cart(self, user_id, items):
        cart, _ = Cart.objects.get_or_create(user_id=user_id)
        CartItem.objects.filter(cart=cart).delete()

        for item in items:
            CartItem.objects.create(
                cart=cart,
                product_id=item["product_id"],
                quantity=item["quantity"],
            )

        # remove the user's flushed cart from dirty cart redis set
        self.cart_redis_service.clear_dirty(user_id)

        