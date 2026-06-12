from .models import Cart, CartItem
from .exceptions import CartNotFoundError, CartItemNotFoundError, InvalidQuantityError
from .cart_redis_service import CartRedisService


class CartService:

    def __init__(self):
        self.redis_service = CartRedisService()

    def get_cart(self, user_id):
        # get the redis cart
        cart = self.redis_service.get_cart_items(user_id)
        return cart

    def add_item(self, user_id, product_id,quantity=1):
        status = self.redis_service.add_item(user_id, product_id, quantity)
        if not status:
            raise Exception("Failed to add item to cart")
        
    def clear_cart(self, user_id):
        status = self.redis_service.clear_cart(user_id)
        if not status:
            raise Exception("Failed to clear cart")
        
    def get_cart_items(self, user_id):
        return self.redis_service.get_cart_items(user_id)
    
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


# class CartItemService:

#     def add_item(self, user_id, product_id, product_name, price_snapshot, quantity=1):
#         cart, _ = Cart.objects.get_or_create(user_id=user_id)
#         existing_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
#         if existing_item:
#             existing_item.quantity += quantity
#             existing_item.save()
#             return existing_item
#         item = CartItem.objects.create(
#             cart=cart,
#             product_id=product_id,
#             product_name=product_name,
#             price_snapshot=price_snapshot,
#             quantity=quantity,
#         )
#         return item

#     def update_item_quantity(self, user_id, item_id, quantity):
#         if quantity < 1:
#             raise InvalidQuantityError("Quantity must be at least 1.")
#         cart = Cart.objects.filter(user_id=user_id).first()
#         if not cart:
#             raise CartNotFoundError(f"Cart for user {user_id} not found.")
#         item = CartItem.objects.filter(id=item_id, cart=cart).first()
#         if not item:
#             raise CartItemNotFoundError(f"Cart item {item_id} not found.")
#         item.quantity = quantity
#         item.save()
#         return item

#     def remove_item(self, user_id, item_id):
#         cart = Cart.objects.filter(user_id=user_id).first()
#         if not cart:
#             raise CartNotFoundError(f"Cart for user {user_id} not found.")
#         item = CartItem.objects.filter(id=item_id, cart=cart).first()
#         if not item:
#             raise CartItemNotFoundError(f"Cart item {item_id} not found.")
#         item.delete()
#         return True
