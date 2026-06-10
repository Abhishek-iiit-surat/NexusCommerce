# Cart Service Architecture

## Overview

Cart service manages user shopping carts. It is a fast, Redis-first service.
PostgreSQL is used only for recovery and analytics — never on the hot path.
Cart stores user intent only: product_id and quantity. No prices, no names.
Display data (name, price, image) comes from Catalog Cache Redis, populated by product-service via Kafka.

---

## Ownership Boundaries

| Concern | Owner |
|---|---|
| User intent (product_id, quantity) | Cart Service — Cart Redis |
| Display data (name, price, image) | Product Service → Catalog Cache Redis |
| Authoritative prices at checkout | Order Service → Product Service |
| Immutable purchase snapshot | Order Service — OrderItem.price_snapshot |
| Cart recovery and analytics | Cart Service — PostgreSQL |

Cart service never calls product-service synchronously on the write path.
Cart service never stores prices as a financial commitment.
Price snapshots are created by order-service at order placement time, not by cart-service.

---

## Redis Key Design

### Cart Hash
```
Key:   cart:{user_id}
Type:  Hash
TTL:   7 days (reset on every mutation)

Field: {product_id}  (string)
Value: JSON string

{
  "quantity": 2,
  "added_at": "2026-06-10T10:00:00Z"
}
```

### Dirty Cart Marker (Sorted Set)
```
Key:   dirty_carts
Type:  Sorted Set
Score: unix timestamp of last mutation
Member: user_id (string)

Written on every cart mutation.
Flush worker reads: ZRANGEBYSCORE dirty_carts 0 <now>
After flush: ZREM dirty_carts {user_id}

DO NOT use SCAN cart:flush:* — SCAN blocks Redis on large keyspaces.
Sorted Set ZRANGEBYSCORE is O(log N + M) where M = only due-for-flush carts.
```

### Catalog Cache (owned by product-service, read by cart-service)
```
Key:   product:{product_id}
Type:  String (JSON)
TTL:   24 hours (reset on every Kafka update)

Value:
{
  "id": 5,
  "name": "Nike Air Max",
  "price": "3999.00",
  "image_url": "https://...",
  "is_active": true,
  "version": 8712
}

Populated by: product-service Kafka consumer (consumers.py)
Read by: cart-service CartRedisService.get_cart()
Version-gated writes: only update if incoming.version > cached.version
```

---

## System Architecture

```
Frontend
    │
    ▼
API Gateway
    │
    ▼
Cart Service (Django, port 8004)
    │
    ├── CartRedisService         ← all API requests go here
    │       │
    │       ├── Cart Redis       ← cart:{user_id} hash
    │       ├── Catalog Redis    ← product:{id} read-only
    │       └── CartPostgresService ← only on cache miss
    │
    └── Celery Worker + Beat
            │
            └── flush_pending_carts (every 60s)
                    │
                    ├── ZRANGEBYSCORE dirty_carts
                    ├── HGETALL cart:{user_id}
                    ├── Bulk upsert → PostgreSQL
                    └── ZREM dirty_carts {user_id}

Product Service (separate)
    │
    ├── On product create/update → Kafka producer publishes product.updated
    └── Kafka consumer → SET product:{id} in Catalog Redis (version-gated)
```

---

## API Endpoints

### Public (authenticated via JWT)

| Method | URL | Description |
|---|---|---|
| GET | `/api/cart/` | Get current user's cart (enriched with catalog data) |
| POST | `/api/cart/items/` | Add item to cart |
| PATCH | `/api/cart/items/{product_id}/` | Update item quantity |
| DELETE | `/api/cart/items/{product_id}/` | Remove item from cart |
| DELETE | `/api/cart/` | Clear entire cart |

Note: URL parameter is `product_id`, not `item_id`. Cart items are keyed by product_id in Redis (Hash field). There is no separate item ID.

### Internal (AllowAny, never exposed via API gateway)

| Method | URL | Description |
|---|---|---|
| GET | `/internal/cart/{user_id}/` | Returns raw cart items for order-service (product_id + quantity only, no enrichment) |
| DELETE | `/internal/cart/{user_id}/` | Clear cart after order confirmed (called by order-service) |

---

## Request/Response Contracts

### POST /api/cart/items/ — Input
```json
{
  "product_id": 5,
  "quantity": 2
}
```
Client never sends price, name, or image. Cart-service never accepts them.

### GET /api/cart/ — Response
```json
{
  "user_id": 42,
  "items": [
    {
      "product_id": 5,
      "quantity": 2,
      "added_at": "2026-06-10T10:00:00Z",
      "name": "Nike Air Max",
      "price": "3999.00",
      "image_url": "https://...",
      "is_active": true,
      "subtotal": "7998.00"
    }
  ],
  "total": "7998.00"
}
```
Name, price, image come from Catalog Cache Redis — not from cart hash, not from product-service HTTP call.

### GET /internal/cart/{user_id}/ — Response (for order-service)
```json
{
  "user_id": 42,
  "items": [
    { "product_id": 5, "quantity": 2 },
    { "product_id": 12, "quantity": 1 }
  ]
}
```
No prices. No names. Order-service resolves prices itself from product-service.

---

## GET /api/cart/ Flow

```
GET /cart/
    │
    ▼
EXISTS cart:{user_id}
    │
    ├── Key missing → PostgreSQL recovery
    │       │
    │       ├── SELECT cart + cart_items WHERE user_id = X
    │       ├── Repopulate Redis: HSET cart:{user_id} + EXPIRE
    │       └── Continue with recovered data
    │
    └── Key exists (even if empty hash) → use Redis data
    │
    ▼
HGETALL cart:{user_id}
    │
    ├── Empty hash → return empty cart (do NOT fall back to PostgreSQL)
    │
    └── Has items
    │
    ▼
Extract product_ids
    │
    ▼
MGET product:5 product:12 product:18   (single Redis round trip)
    │
    ├── All hits → merge and return
    │
    └── Any miss → GET /internal/products/{id}/ from product-service
                 → SET product:{id} EX 86400 in catalog Redis
                 → merge and return
```

Key rule: empty hash means genuinely empty cart. Missing key means unknown state → attempt recovery.

---

## Add Item Flow

```
POST /cart/items/ { product_id: 5, quantity: 2 }
    │
    ▼
Validate: product_id (int), quantity (int, min=1)
    │
    ▼
HSET cart:{user_id} "5" '{"quantity":2,"added_at":"..."}'
EXPIRE cart:{user_id} 604800
    │
    ▼
ZADD dirty_carts <now_timestamp> {user_id}
    │
    ▼
Return 201
```

No product-service call. No PostgreSQL call. No Kafka. Just Redis.
Total latency target: < 5ms.

If product_id already exists in cart hash → update quantity (add to existing, do not replace).

---

## Flush Flow (Background)

```
Celery Beat — every 60 seconds
    │
    ▼
flush_pending_carts task
    │
    ▼
ZRANGEBYSCORE dirty_carts 0 <now>
    │
    ├── Empty → nothing to flush, exit
    │
    └── Returns [user_id_1, user_id_2, ...]
    │
    ▼
For each user_id:
    HGETALL cart:{user_id}
    │
    ├── Empty → cart was cleared, delete PostgreSQL cart_items, ZREM
    │
    └── Has items →
            BEGIN TRANSACTION
            DELETE FROM cart_items WHERE cart.user_id = X
            bulk_create(CartItem list)
            COMMIT
            ZREM dirty_carts {user_id}
```

Bulk upsert strategy: delete-then-bulk-insert in a single transaction.
Never use N individual update_or_create calls — that is N round trips to PostgreSQL.

---

## Checkout Flow (Order Placement)

```
User clicks "Place Order"
    │
    ▼
Order Service receives POST /orders/
    │
    ▼
Order Service calls GET /internal/cart/{user_id}/   (cart-service)
    │   returns: [{ product_id, quantity }]
    │
    ▼
Order Service calls product-service for current prices
    │   builds OrderItem with price_snapshot (immutable from this point)
    │
    ▼
Order Service calls inventory-service (stock check + reservation)
    │
    ▼
Order Service saves Order + OrderItems to PostgreSQL
    │   status = PENDING_PAYMENT
    │
    ▼
Order Service calls DELETE /internal/cart/{user_id}/   (cart-service)
    │   cart-service: DEL cart:{user_id}, ZREM dirty_carts {user_id}
    │   cart-service: DELETE cart_items from PostgreSQL
    │
    ▼
Order Service publishes order.expiry.scheduled to Kafka
```

Cart is cleared only after order is successfully saved. Never before.
If order creation fails, cart remains intact. User can retry.

---

## Catalog Cache — How It Gets Populated

This is owned by product-service, not cart-service. Documented here for context.

```
Admin updates product price
    │
    ▼
product-service saves to product_db
    │
    ▼
product-service Kafka producer publishes:
topic: product.updated
{
  "id": 5,
  "name": "Nike Air Max",
  "price": "4499.00",
  "image_url": "...",
  "is_active": true,
  "version": 8713
}
    │
    ▼
product-service Kafka consumer receives event
    │
    ▼
GET product:5 from Redis → check cached version
    │
    ├── incoming.version > cached.version → SET product:5 EX 86400
    └── incoming.version <= cached.version → discard (out-of-order delivery)
```

Nightly full sync job (product-service) rebuilds entire catalog cache from PostgreSQL as safety net.
If catalog Redis is fully lost, first cart GET causes HTTP fallback to product-service, which repopulates.

---

## File Structure

```
services/cart-service/
├── apps/cart/
│   ├── cart_redis_service.py       ← Phase 1: all Redis operations
│   ├── cart_postgres_service.py    ← Phase 2: flush + recovery
│   ├── catalog_cache_service.py    ← Phase 3: MGET + cache miss fallback
│   ├── clients/
│   │   └── product_client.py       ← Phase 3: HTTP fallback to product-service
│   ├── tasks.py                    ← Phase 2: Celery flush task
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── models.py                   ← Cart + CartItem (PostgreSQL, recovery only)
│   ├── authentication.py           ← JWTUserAuthentication (no DB hit)
│   ├── exceptions.py               ← CartNotFoundError, CartItemNotFoundError, etc.
│   ├── consumers.py                ← Phase 3+: future Kafka consumers if needed
│   └── producers.py                ← Phase 3+: future Kafka producers if needed
├── config/
│   ├── celery.py                   ← Celery app setup
│   ├── settings/
│   │   └── base.py                 ← Redis, Celery, DB config
│   └── urls.py
└── ARCHITECTURE.md                 ← this file
```

---

## Build Phases

### Phase 1 — Redis-only cart (build now)
- `cart_redis_service.py`: add_item, update_quantity, remove_item, get_cart_items, clear_cart, cart_exists
- `serializers.py`: AddCartItemSerializer (product_id + quantity), CartResponseSerializer
- `views.py`: all 5 public endpoints + 2 internal endpoints
- `urls.py`: updated routes using product_id not item_id

### Phase 2 — Persistence (build after Phase 1 works)
- `cart_postgres_service.py`: flush_cart (delete + bulk_create), recover_cart, repopulate_redis
- `tasks.py`: flush_pending_carts Celery task
- `config/celery.py`: Celery app
- Docker: add cart-worker and cart-beat containers

### Phase 3 — Catalog cache enrichment (build after product-service has Kafka producer)
- `catalog_cache_service.py`: get_products_from_cache, handle_cache_miss
- `clients/product_client.py`: HTTP fallback with timeout + error handling
- Wire into get_cart() response enrichment

### Phase 4 — Checkout integration (build when order-service services.py is ready)
- Internal endpoints already exist from Phase 1
- Order-service calls them — no cart-service changes needed
- Verify force-clear on order confirmation works correctly

---

## Key Invariants (never violate these)

1. Client never sends price to cart-service under any circumstance
2. Empty hash and missing key are different states — treat them differently
3. SCAN is never used — always ZRANGEBYSCORE on dirty_carts sorted set
4. PostgreSQL is never written on the API request path — only by Celery flush task
5. Cart is cleared only after order is successfully persisted, never before
6. Catalog cache writes are version-gated — lower version is always discarded
7. Internal endpoints are AllowAny but must never be registered in API gateway routing
