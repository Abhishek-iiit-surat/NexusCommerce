import json
import time
import redis
from django.conf import settings

CART_TTL = 7 * 24 * 60 * 60  # 7 days in seconds


def _get_redis():
    return redis.from_url(settings.REDIS_URL, decode_responses=True)


def _cart_key(user_id):
    return f"cart:{user_id}"


class CartRedisService:

    def __init__(self):
        self.r = _get_redis()

    def cart_exists(self, user_id):
        return self.r.exists(_cart_key(user_id)) == 1

    def add_item(self, user_id, product_id, quantity):
        key = _cart_key(user_id)
        product_id_str = str(product_id)

        existing_raw = self.r.hget(key, product_id_str)
        if existing_raw:
            existing = json.loads(existing_raw)
            new_quantity = existing["quantity"] + quantity
        else:
            new_quantity = quantity

        value = json.dumps({
            "quantity": new_quantity,
            "added_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        })
        self.r.hset(key, product_id_str, value)
        self.r.expire(key, CART_TTL)
        self._mark_dirty(user_id)

    def update_quantity(self, user_id, product_id, quantity):
        key = _cart_key(user_id)
        product_id_str = str(product_id)

        existing_raw = self.r.hget(key, product_id_str)
        if not existing_raw:
            return False  # item not in cart

        existing = json.loads(existing_raw)
        value = json.dumps({
            "quantity": quantity,
            "added_at": existing["added_at"],
        })
        self.r.hset(key, product_id_str, value)
        self.r.expire(key, CART_TTL)
        self._mark_dirty(user_id)
        return True

    def remove_item(self, user_id, product_id):
        key = _cart_key(user_id)
        removed = self.r.hdel(key, str(product_id))
        if removed:
            self.r.expire(key, CART_TTL)
            self._mark_dirty(user_id)
        return removed > 0

    def get_cart_items(self, user_id):
        """
        Returns list of dicts: [{product_id, quantity, added_at}]
        Empty list means cart is empty (not the same as cart not existing).
        """
        raw = self.r.hgetall(_cart_key(user_id))
        items = []
        for product_id_str, value_json in raw.items():
            data = json.loads(value_json)
            items.append({
                "product_id": int(product_id_str),
                "quantity": data["quantity"],
                "added_at": data["added_at"],
            })
        return items

    def clear_cart(self, user_id):
        key = _cart_key(user_id)
        existing_fields = self.r.hkeys(key)
        if existing_fields:
            self.r.hdel(key, *existing_fields)
        self.r.expire(key, CART_TTL)
        self._mark_dirty(user_id)

    def repopulate_from_items(self, user_id, items):
        """
        Used by CartPostgresService during recovery.
        items: list of dicts with product_id, quantity, added_at
        """
        key = _cart_key(user_id)
        mapping = {}
        for item in items:
            mapping[str(item["product_id"])] = json.dumps({
                "quantity": item["quantity"],
                "added_at": str(item["added_at"]),
            })
        if mapping:
            self.r.hset(key, mapping=mapping)
        self.r.expire(key, CART_TTL)

    def _mark_dirty(self, user_id):
        self.r.zadd("dirty_carts", {str(user_id): time.time()})
