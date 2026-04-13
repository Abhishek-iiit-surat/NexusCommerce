<div align="center">

```
███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗
██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║
██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║
╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝
     ██████╗ ██████╗ ███╗   ███╗███╗   ███╗███████╗██████╗  ██████╗███████╗
    ██╔════╝██╔═══██╗████╗ ████║████╗ ████║██╔════╝██╔══██╗██╔════╝██╔════╝
    ██║     ██║   ██║██╔████╔██║██╔████╔██║█████╗  ██████╔╝██║     █████╗
    ██║     ██║   ██║██║╚██╔╝██║██║╚██╔╝██║██╔══╝  ██╔══██╗██║     ██╔══╝
    ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║ ╚═╝ ██║███████╗██║  ██║╚██████╗███████╗
     ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝╚══════╝
```

**Production-grade e-commerce backend engineered for scale.**

A distributed microservices platform built with Django, Kafka, Kubernetes, and gRPC —
covering every advanced backend concept a senior engineer expects in 2024–25.

<br/>

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com)
[![Kafka](https://img.shields.io/badge/Apache_Kafka-2.8-231F20?style=for-the-badge&logo=apachekafka&logoColor=white)](https://kafka.apache.org)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-1.28-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)](https://kubernetes.io)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Redis](https://img.shields.io/badge/Redis-7.0-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io)
[![Terraform](https://img.shields.io/badge/Terraform-1.6-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)](https://terraform.io)
[![Docker](https://img.shields.io/badge/Docker-24.0-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)

<br/>

</div>

---

## 📖 What Is This?

**Nexus Commerce** is not a tutorial project. It is a deliberate attempt to build a backend system the way it would be built at a well-engineered company — with the patterns, tooling, and operational maturity that separate junior developers from senior engineers.

The project covers 15 microservices, an event-driven architecture with Apache Kafka, distributed transaction management via the Saga pattern, gRPC for inter-service communication, full observability with OpenTelemetry + Jaeger + Prometheus, and a production-grade CI/CD pipeline deploying to Kubernetes via GitHub Actions.

Every architectural decision has a reason. Every pattern solves a real problem.

---

## 🏗️ Architecture Overview

```
                              ┌─────────────────────────────────────┐
                              │           CLIENT (Web / Mobile)     │
                              └──────────────────┬──────────────────┘
                                                 │ HTTPS
                              ┌──────────────────▼──────────────────┐
                              │              API GATEWAY             │
                              │   Rate Limiting · Auth · Routing    │
                              └──┬──────┬──────┬──────┬──────┬──────┘
                                 │      │      │      │      │
                          REST / gRPC (internal services communicate via gRPC)
                                 │      │      │      │      │
              ┌──────────────────┘      │      │      │      └─────────────────┐
              │                         │      │      │                        │
   ┌──────────▼──────┐    ┌─────────────▼──┐   │   ┌──▼──────────────┐  ┌────▼──────────┐
   │  auth-service   │    │ product-service │   │   │  order-service  │  │ cart-service  │
   │  PostgreSQL     │    │  PostgreSQL     │   │   │  PostgreSQL     │  │  Redis        │
   └─────────────────┘    └────────────────┘   │   └────────┬────────┘  └───────────────┘
                                                │            │
                                     ┌──────────▼──────────────────────────────┐
                                     │           APACHE KAFKA                  │
                                     │  Event Backbone · 13 Topics · DLQ      │
                                     └──┬──────┬──────┬──────┬──────┬─────────┘
                                        │      │      │      │      │
                           ┌────────────┘   ┌──┘      └──┐   └──────────────┐
                           │                │             │                  │
              ┌────────────▼───┐  ┌─────────▼───┐  ┌────▼──────────┐  ┌───▼────────────┐
              │inventory-svc   │  │payment-svc  │  │notification   │  │analytics-svc   │
              │PostgreSQL      │  │PostgreSQL   │  │svc            │  │ClickHouse      │
              └────────────────┘  └─────────────┘  └───────────────┘  └────────────────┘
```

---

## 🧩 The 15 Microservices

| Service | Responsibility | DB | Port |
|---|---|---|---|
| `api-gateway` | Auth validation, routing, rate limiting, BFF | — | 8000 |
| `auth-service` | JWT, OAuth2, refresh tokens, TOTP 2FA, RBAC | PostgreSQL | 8001 |
| `user-service` | Profiles, addresses, preferences | PostgreSQL | 8002 |
| `product-service` | Catalog, variants, pricing tiers, audit logs | PostgreSQL | 8003 |
| `inventory-service` | Stock levels, reservations, multi-warehouse | PostgreSQL | 8004 |
| `order-service` | Order lifecycle, Saga orchestration, CQRS | PostgreSQL + MongoDB | 8005 |
| `payment-service` | Stripe integration, refunds, Event Sourcing | PostgreSQL | 8006 |
| `cart-service` | Redis-backed cart, promo codes, price sync | Redis | 8007 |
| `notification-service` | Email, SMS, push, in-app via Kafka events | PostgreSQL | 8008 |
| `search-service` | Elasticsearch full-text, facets, autocomplete | Elasticsearch | 8009 |
| `review-service` | Ratings, moderation, aggregates | PostgreSQL | 8010 |
| `recommendation-service` | Personalized suggestions | MongoDB | 8011 |
| `analytics-service` | Event tracking, dashboards, funnels | ClickHouse | 8012 |
| `file-service` | Presigned uploads, image compression, CDN | PostgreSQL + MinIO | 8013 |
| `admin-service` | Seller portal, ops dashboard | PostgreSQL | 8014 |

---

## ⚙️ Technical Concepts Implemented

### Distributed Systems Patterns
- **Saga Pattern (Choreography)** — distributed transactions across order → inventory → payment → notification with compensating transactions on failure
- **Outbox Pattern** — zero message loss by writing events to DB and Kafka in a single transaction
- **Idempotent Consumers** — all Kafka consumers are safe to retry; duplicate events never cause double processing
- **CQRS** — separate read/write models on order-service (PostgreSQL writes, MongoDB reads)
- **Event Sourcing** — payment-service never updates records; state is reconstructed by replaying events
- **Change Data Capture** — Debezium streams all DB changes to Kafka automatically; used to keep Elasticsearch in sync

### Performance & Scalability
- **Redis caching** with cache-aside pattern, TTL, and event-driven cache invalidation
- **Cursor-based pagination** on all list endpoints (offset pagination breaks at scale)
- **Database read replicas** for analytics queries
- **PgBouncer** for connection pooling
- **select_for_update()** and optimistic locking to prevent race conditions
- **Stock reservation TTL** — abandoned carts auto-release stock via Celery

### Security
- JWT with short-lived access tokens + rotating refresh tokens
- RBAC with granular permissions (`product:write`, `order:cancel`, etc.)
- TOTP-based 2FA compatible with Google Authenticator
- Redis sliding window rate limiting per IP and per user
- Brute force protection with account lockout
- HashiCorp Vault for secrets — no `.env` files in production
- OAuth2 social login (Google, GitHub)
- Magic byte validation on file uploads (not just Content-Type header)
- Presigned URLs — file bytes never pass through application servers

### Observability
- **Structured JSON logging** with `structlog` — every log has correlation ID, service name, user ID
- **Correlation ID** injected at API gateway and propagated through every downstream service
- **Distributed tracing** with OpenTelemetry + Jaeger — trace a single order across all 15 services
- **Custom Prometheus metrics** — `orders_placed_total`, `payment_failures_total`, `cart_abandonment_rate`
- **Grafana dashboards** — service health, business metrics, infrastructure
- **Sentry** for error tracking with full context

### Infrastructure & Deployment
- **Kubernetes** with HPA, PodDisruptionBudgets, rolling updates
- **Istio service mesh** — mTLS between all services, canary deployments, circuit breakers
- **Helm charts** per service with environment-specific values
- **Terraform** for all infrastructure — VPC, EKS, RDS, ElastiCache, MSK
- **GitHub Actions CI/CD** — lint → test → scan → staging → manual approval → canary → prod
- **Trivy** Docker image vulnerability scanning in pipeline
- **Canary deployments** with auto-rollback on error rate spike

---

## 🗂️ Repository Structure

```
nexus-commerce/
├── services/
│   ├── auth-service/
│   │   ├── apps/
│   │   │   └── authentication/
│   │   │       ├── models.py
│   │   │       ├── serializers.py
│   │   │       ├── views.py
│   │   │       ├── services.py        ← business logic
│   │   │       ├── repositories.py   ← data access layer
│   │   │       ├── consumers.py      ← kafka consumers
│   │   │       ├── producers.py      ← kafka producers
│   │   │       └── tests/
│   │   ├── config/
│   │   │   └── settings/
│   │   │       ├── base.py
│   │   │       ├── development.py
│   │   │       └── production.py
│   │   └── Dockerfile
│   ├── product-service/
│   ├── order-service/
│   └── ... (same structure × 15)
│
├── shared/
│   ├── proto/                        ← gRPC proto definitions
│   ├── events/                       ← Kafka event schemas
│   └── middleware/                   ← shared Django middleware
│
├── infrastructure/
│   ├── docker/
│   ├── kubernetes/
│   │   ├── namespaces/
│   │   └── services/
│   │       └── order-service/
│   │           ├── deployment.yaml
│   │           ├── service.yaml
│   │           └── hpa.yaml
│   ├── terraform/
│   │   ├── modules/
│   │   │   ├── rds/
│   │   │   ├── eks/
│   │   │   └── elasticache/
│   │   └── environments/
│   │       ├── dev/
│   │       ├── staging/
│   │       └── prod/
│   └── helm/
│
├── docs/
│   ├── adr/                          ← Architecture Decision Records
│   │   ├── 001-why-kafka-over-rabbitmq.md
│   │   ├── 002-outbox-pattern.md
│   │   └── 003-saga-choreography-vs-orchestration.md
│   └── diagrams/
│
├── tests/
│   ├── integration/                  ← Testcontainers
│   ├── contract/                     ← Pact
│   └── load/                         ← k6 scripts
│
├── docker-compose.yml
├── docker-compose.dev.yml
├── Makefile
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Docker 24+ and Docker Compose
- Python 3.11+
- Make

### Run locally

```bash
# Clone the repo
git clone https://github.com/yourusername/nexus-commerce.git
cd nexus-commerce

# Start all services
make up

# Run migrations for all services
make migrate-all

# Tail logs for a specific service
make logs service=order-service

# Open a Django shell in a service
make shell service=product-service
```

### Verify everything is running

```bash
# API Gateway health
curl http://localhost:8000/health

# Kafka topics
docker exec -it kafka kafka-topics.sh --list --bootstrap-server localhost:9092

# Elasticsearch
curl http://localhost:9200/_cat/indices

# Jaeger UI
open http://localhost:16686

# Grafana
open http://localhost:3000   # admin / admin

# MinIO Console
open http://localhost:9001
```

---

## 🌊 The Order Flow (End-to-End)

This is the most complex flow in the system — it touches 7 services, 4 databases, Kafka, gRPC, and the Saga pattern.

```
1. POST /orders  (api-gateway → order-service)
   └── order-service creates Order (status: PENDING)
   └── Writes OrderCreated event to Outbox table
   └── Celery publishes Outbox → Kafka: ecommerce.orders.created

2. inventory-service consumes ecommerce.orders.created
   └── Calls select_for_update() on inventory rows
   └── Reserves stock for each SKU
   └── Publishes: ecommerce.inventory.reserved

3. payment-service consumes ecommerce.inventory.reserved
   └── Charges card via Stripe (idempotency key = order_id)
   └── Appends PaymentCharged event (Event Sourcing)
   └── Publishes: ecommerce.payments.charged

4. order-service consumes ecommerce.payments.charged
   └── Updates order status → CONFIRMED
   └── Syncs read model to MongoDB (CQRS)
   └── Publishes: ecommerce.orders.confirmed

5. notification-service consumes ecommerce.orders.confirmed
   └── Sends confirmation email + push notification

6. analytics-service consumes ecommerce.orders.confirmed
   └── Writes conversion event to ClickHouse

── IF PAYMENT FAILS ──────────────────────────────────────────────

3b. payment-service publishes: ecommerce.payments.failed

4b. inventory-service consumes ecommerce.payments.failed
    └── Releases stock reservation (compensating transaction)

5b. order-service consumes ecommerce.payments.failed
    └── Updates order status → CANCELLED

6b. notification-service sends cancellation email
```

---

## 📊 Kafka Topics

| Topic | Producer | Consumers |
|---|---|---|
| `ecommerce.orders.created` | order-service | inventory-service |
| `ecommerce.orders.confirmed` | order-service | notification-service, analytics-service |
| `ecommerce.orders.cancelled` | order-service | notification-service, analytics-service |
| `ecommerce.inventory.reserved` | inventory-service | payment-service |
| `ecommerce.inventory.released` | inventory-service | order-service |
| `ecommerce.inventory.low_stock` | inventory-service | notification-service, admin-service |
| `ecommerce.payments.charged` | payment-service | order-service |
| `ecommerce.payments.failed` | payment-service | inventory-service, order-service |
| `ecommerce.payments.refunded` | payment-service | order-service, notification-service |
| `ecommerce.products.updated` | product-service | search-service (re-index) |
| `ecommerce.users.registered` | auth-service | notification-service |
| `ecommerce.notifications.send` | multiple | notification-service |
| `ecommerce.analytics.events` | multiple | analytics-service |

All topics have a corresponding **Dead Letter Queue** (`*.dlq`) for failed messages.

---

## 🧪 Testing

```bash
# Unit tests for a service
make test service=order-service

# Integration tests (spins up real Postgres + Redis via Testcontainers)
make test-integration service=order-service

# Contract tests (Pact — verifies service boundaries)
make test-contract

# Load test (k6 — simulates 1000 concurrent users placing orders)
make load-test

# Security scan (OWASP ZAP)
make security-scan
```

### Test coverage targets

| Layer | Tool | Target |
|---|---|---|
| Unit | pytest | 80%+ |
| Integration | pytest + Testcontainers | All DB / cache operations |
| Contract | Pact | All service-to-service calls |
| Load | k6 | p99 < 500ms at 1000 concurrent users |
| Security | OWASP ZAP | All public endpoints |

---

## 🔭 Observability

### Distributed Tracing (Jaeger)

Every request gets a `X-Correlation-ID` at the API gateway. This ID is propagated through every service call, Kafka message, and log entry — allowing you to trace a single user's order across all 15 services in Jaeger.

```
http://localhost:16686
```

### Metrics (Prometheus + Grafana)

Dashboards available at `http://localhost:3000`:

- **Service Health** — request rate, error rate, p50/p95/p99 latency per service
- **Business Metrics** — orders/min, revenue/hour, cart abandonment rate
- **Infrastructure** — CPU, memory, DB connections, Kafka consumer lag
- **Kafka** — messages/sec per topic, consumer lag, DLQ depth

### Alerting Rules

| Alert | Condition |
|---|---|
| High error rate | Error rate > 1% over 5 minutes |
| Slow responses | p99 latency > 500ms |
| Kafka lag | Consumer lag > 1000 messages |
| Low stock | Available stock < 10 units |
| Payment failures | Failure rate > 2% |

---

## 🏛️ Architecture Decision Records

Key architectural decisions are documented in `/docs/adr/`:

- [ADR-001: Why Kafka over RabbitMQ](./docs/adr/001-why-kafka-over-rabbitmq.md)
- [ADR-002: Outbox Pattern for reliable event publishing](./docs/adr/002-outbox-pattern.md)
- [ADR-003: Saga choreography vs orchestration](./docs/adr/003-saga-choreography-vs-orchestration.md)
- [ADR-004: CQRS on order-service](./docs/adr/004-cqrs-order-service.md)
- [ADR-005: Event Sourcing on payment-service](./docs/adr/005-event-sourcing-payments.md)
- [ADR-006: Cursor-based pagination](./docs/adr/006-cursor-pagination.md)
- [ADR-007: Why Django over Go/Node for microservices](./docs/adr/007-django-for-microservices.md)

---

## 🗺️ Build Roadmap

| Phase | Focus | Status |
|---|---|---|
| 1 | Project foundation, monorepo, Docker Compose | 🔄 In Progress |
| 2 | Auth & Security (JWT, RBAC, 2FA, Vault) | ⏳ Pending |
| 3 | Core microservices (product, inventory, cart, order) | ⏳ Pending |
| 4 | Async messaging with Kafka + Outbox Pattern | ⏳ Pending |
| 5 | Distributed transactions & Saga Pattern | ⏳ Pending |
| 6 | gRPC internal communication | ⏳ Pending |
| 7 | Search (Elasticsearch) & performance | ⏳ Pending |
| 8 | File service & media handling | ⏳ Pending |
| 9 | Observability (OTel, Jaeger, Prometheus, Grafana) | ⏳ Pending |
| 10 | Kubernetes + Istio service mesh | ⏳ Pending |
| 11 | CI/CD with GitHub Actions | ⏳ Pending |
| 12 | Advanced patterns (CQRS, Event Sourcing, CDC) | ⏳ Pending |
| 13 | Infrastructure as Code (Terraform) | ⏳ Pending |
| 14 | Testing strategy (unit, integration, contract, load) | ⏳ Ongoing |

---

## 🛠️ Full Tech Stack

```
Language & Framework   Python 3.11 · Django 4.2 · Django REST Framework
API Gateway            Custom Django · Kong (production)
Authentication         JWT · OAuth2 · TOTP · HashiCorp Vault
Databases              PostgreSQL 15 · Redis 7 · MongoDB · Elasticsearch 8 · ClickHouse
Message Broker         Apache Kafka · Zookeeper
Inter-service RPC      gRPC · Protocol Buffers
File Storage           MinIO (S3-compatible)
Task Queue             Celery · Redis
Containers             Docker · Kubernetes 1.28
Service Mesh           Istio
Infrastructure         Terraform · Helm
CI/CD                  GitHub Actions
Observability          OpenTelemetry · Jaeger · Prometheus · Grafana · Sentry
CDC                    Debezium
Testing                pytest · Testcontainers · Pact · k6 · OWASP ZAP
```

---

## 📄 License

MIT License — see [LICENSE](./LICENSE) for details.

---

<div align="center">

Built to learn. Engineered to impress.

</div>
