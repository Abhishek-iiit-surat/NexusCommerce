import logging

from celery import shared_task

from .cart_redis_service import CartRedisService
from .cart_postgres_service import CartPostgresService

logger = logging.getLogger(__name__)


@shared_task
def flush_pending_carts():
    """
    Celery Beat task, runs every 60s (see CELERY_BEAT_SCHEDULE in settings).

    For each user_id due in the dirty_carts sorted set: read their current
    items from Redis, flush them to Postgres, then clear their dirty flag.
    Each user is isolated in its own try/except so one failure doesn't
    stop the rest of the batch from flushing.
    """
    redis_service = CartRedisService()
    postgres_service = CartPostgresService()
    dirty_users = redis_service.get_dirty_carts()

    if not dirty_users:
        return

    for user in dirty_users:
        try:
            items = redis_service.get_cart_items(user)
            postgres_service.flush_cart(user, items)
            redis_service.clear_dirty(user)
        except Exception:
            logger.exception("Failed to flush cart for user_id=%s", user)
