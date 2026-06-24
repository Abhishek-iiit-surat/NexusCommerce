from django.db import transaction
from django.db.models import F
from .models import Cart, CartItem


class CartPostgresService:

    def flush_cart(self, user_id, items):
        """
        Replace the user's stored cart items with the current Redis state.
        Get-or-create + delete + bulk_create run atomically so a crash
        mid-flush can't leave the cart half-written.
        """
        with transaction.atomic():
            cart, _ = Cart.objects.get_or_create(user_id=user_id)
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

    def recover_cart(self, user_id):
        cart = Cart.objects.filter(user_id=user_id).first()
        return list(
            cart.items.annotate(added_at=F("updated_at"))
            .values(
                "product_id",
                "quantity",
                "added_at"
            )
        ) if cart else []

        