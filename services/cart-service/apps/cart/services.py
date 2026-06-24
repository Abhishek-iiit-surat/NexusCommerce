from .exceptions import CartNotFoundError, CartItemNotFoundError, InvalidQuantityError, UnexpectedError
from .cart_redis_service import CartRedisService
from .cart_postgres_service import CartPostgresService


class CartService:

    def __init__(self):
        self.redis_service = CartRedisService()
        self.postgres_service = CartPostgresService()

    def get_cart(self, user_id):
        # get the redis cart
        if not self.redis_service.cart_exists(user_id):
            items = self.postgres_service.recover_cart(user_id)
            self.redis_service.repopulate_from_items(user_id, items)
        return self.redis_service.get_cart_items(user_id)

    def add_item(self, user_id, product_id,quantity=1):
        status = self.redis_service.add_item(user_id, product_id, quantity)
        if not status:
            raise UnexpectedError("Failed to add item in the cart")
        
    def clear_cart(self, user_id):
        status = self.redis_service.clear_cart(user_id)
        if not status:
            raise UnexpectedError("Failed to clear cart")
    
    def remove_item(self, user_id, product_id):
        status = self.redis_service.remove_item(user_id, product_id)
        if not status:
            raise CartItemNotFoundError(f"Product {product_id} not found in cart.")
        
    def update_item_quantity(self, user_id, product_id, quantity):
        if quantity < 1:
            raise InvalidQuantityError("Quantity must be at least 1.")
        status = self.redis_service.update_quantity(user_id, product_id, quantity)
        if not status:
            raise CartItemNotFoundError(f"Product {product_id} not found in cart.")
