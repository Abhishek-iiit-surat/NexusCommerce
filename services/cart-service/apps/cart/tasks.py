from celery import shared_task

from .cart_redis_service import CartRedisService
from .cart_postgres_service import CartPostgresService  


@shared_task
def flush_pending_carts():
   """
    Celery Beat task, runs every 60s (see CELERY_BEAT_SCHEDULE in settings).

    Steps (see ARCHITECTURE.md "Flush Flow"):
    1. Get due user_ids from the dirty_carts sorted set (ZRANGEBYSCORE 0 <now>).
       TODO: CartRedisService has no public method for this yet — only the
       private _mark_dirty() writer. Add one (e.g. get_dirty_user_ids()).

    2. If nothing is due, return early.

    3. For each user_id:
       - Read current items from Redis (CartRedisService.get_cart_items).
       - Hand them to CartPostgresService.flush_cart(user_id, items).
       - Remove the user_id from dirty_carts so it isn't flushed again
         next cycle (needs a ZREM method too).
   """
   redis_service = CartRedisService()
   postgres_service = CartPostgresService()
   dirty_users = redis_service.get_dirty_carts()

   if not dirty_users:
      return
   
   for user in dirty_users:
      items = redis_service.get_cart_items(user)
      postgres_service.flush_cart(user, items)
