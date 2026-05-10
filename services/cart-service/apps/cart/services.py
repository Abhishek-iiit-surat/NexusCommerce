from .models import Cart, CartItem
from .exceptions import CartNotFoundError, CartItemNotFoundError, InvalidQuantityError


class CartService:

    def get_or_create_cart(self, user_id):
        cart, _ = Cart.objects.get_or_create(user_id=user_id)
        return cart

    def get_cart(self, user_id):
        cart = Cart.objects.filter(user_id=user_id).first()
        if not cart:
            raise CartNotFoundError(f"Cart for user {user_id} not found.")
        return cart

    def clear_cart(self, user_id):
        cart = self.get_cart(user_id)
        cart.items.all().delete()
        return cart


class CartItemService:

    def add_item(self, user_id, product_id, product_name, price_snapshot, quantity=1):
        cart, _ = Cart.objects.get_or_create(user_id=user_id)
        existing_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
        if existing_item:
            existing_item.quantity += quantity
            existing_item.save()
            return existing_item
        item = CartItem.objects.create(
            cart=cart,
            product_id=product_id,
            product_name=product_name,
            price_snapshot=price_snapshot,
            quantity=quantity,
        )
        return item

    def update_item_quantity(self, user_id, item_id, quantity):
        if quantity < 1:
            raise InvalidQuantityError("Quantity must be at least 1.")
        cart = Cart.objects.filter(user_id=user_id).first()
        if not cart:
            raise CartNotFoundError(f"Cart for user {user_id} not found.")
        item = CartItem.objects.filter(id=item_id, cart=cart).first()
        if not item:
            raise CartItemNotFoundError(f"Cart item {item_id} not found.")
        item.quantity = quantity
        item.save()
        return item

    def remove_item(self, user_id, item_id):
        cart = Cart.objects.filter(user_id=user_id).first()
        if not cart:
            raise CartNotFoundError(f"Cart for user {user_id} not found.")
        item = CartItem.objects.filter(id=item_id, cart=cart).first()
        if not item:
            raise CartItemNotFoundError(f"Cart item {item_id} not found.")
        item.delete()
        return True
