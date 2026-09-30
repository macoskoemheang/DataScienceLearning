# 🛒 POS Shop API

A RESTful Point-of-Sale API for a general shop, built with **Flask**, **SQLAlchemy**, and **JWT authentication** (with role-based access control), documented with an interactive **Swagger UI**. Ready to run on **SQLite** locally or **Supabase Postgres** in production.

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0-black.svg)
![JWT](https://img.shields.io/badge/auth-JWT-orange.svg)
![Supabase](https://img.shields.io/badge/db-Supabase%20%2F%20SQLite-3ecf8e.svg)

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Roles & Permissions](#roles--permissions)
- [API Documentation](#api-documentation)
- [Authentication Flow](#authentication-flow)
- [API Reference](#api-reference)
- [Pagination & Filtering](#pagination--filtering)
- [Dashboard / Analytics](#dashboard--analytics)
- [CORS (for a web portal)](#cors-for-a-web-portal)
- [Example Requests](#example-requests)
- [Migrating to Supabase](#migrating-to-supabase)
- [Notes](#notes)

## Features

- 🔐 JWT-based authentication with **admin / cashier** roles
- 📦 Product & category management with stock tracking
- 🧾 Checkout flow: cart → sale, with automatic stock decrement
- 👥 Customer records linked to sales
- 👤 Employee management: create staff with a role, deactivate access (no hard delete — history stays intact)
- 📊 Dashboard endpoints: revenue summary, top-selling products, low-stock alerts, recent sales
- 🔎 Pagination + search on products/customers/sales, for building portal tables
- 🌐 CORS enabled — ready to be called from a separate web dashboard
- 📑 Interactive Swagger UI, generated from route docstrings
- 💾 SQLite for local dev, drop-in Supabase/Postgres for production

## Tech Stack

| Layer          | Technology              |
|----------------|--------------------------|
| Language       | Python 3.11+             |
| Framework      | Flask 3.0                |
| ORM            | Flask-SQLAlchemy         |
| Database       | SQLite (dev) / Supabase Postgres (prod) |
| DB driver      | psycopg 3                |
| Auth           | Flask-JWT-Extended       |
| API Docs       | Flasgger (Swagger UI)    |

## Architecture

The project follows **Clean Architecture**: dependencies point inward, and
business logic has no idea Flask or SQLAlchemy exist.

```
 ┌─────────────────────────────────────────────────────────┐
 │  interfaces/http        Flask blueprints, JSON in/out    │
 │  ┌───────────────────────────────────────────────────┐  │
 │  │  infrastructure       SQLAlchemy models & repos     │  │
 │  │  ┌─────────────────────────────────────────────┐  │  │
 │  │  │  application        Use cases (business flow) │  │  │
 │  │  │  ┌───────────────────────────────────────┐  │  │  │
 │  │  │  │  domain    Entities & repository ports │  │  │  │
 │  │  │  └───────────────────────────────────────┘  │  │  │
 │  │  └─────────────────────────────────────────────┘  │  │
 │  └───────────────────────────────────────────────────┘  │
 └─────────────────────────────────────────────────────────┘
```

- **`domain`** — plain Python entities (`User`, `Category`, `Product`,
  `Customer`, `Sale`/`SaleItem`) and abstract repository interfaces
  (ports). No Flask, no SQLAlchemy.
- **`application`** — use cases (`CreateSaleUseCase`, `CreateProductUseCase`,
  ...) that implement business rules against the repository *interfaces*,
  and raise framework-agnostic exceptions (`ValidationError`, `NotFoundError`, ...).
  This is where checkout logic lives: validating stock, snapshotting unit
  prices, and computing totals.
- **`infrastructure`** — concrete adapters: SQLAlchemy models and
  repository implementations that satisfy the domain ports. `create_sale`
  here also applies stock decrements atomically in the same transaction.
- **`interfaces/http`** — Flask blueprints that parse requests, call a use
  case, catch its exceptions, and translate them into HTTP responses. Also
  where role-based access control (`@role_required`) is enforced.

This means the storage engine (SQLite → Supabase) or the web framework
could be swapped without touching a single use case.

## Project Structure

```
flask-rest-api/
├── app/
│   ├── __init__.py                          # create_app(): wires everything together
│   ├── config.py                            # Config class (reads .env, DATABASE_URL, JWT secret)
│   ├── domain/
│   │   ├── entities/
│   │   │   ├── user.py                      # User entity (username, role: admin/cashier)
│   │   │   ├── category.py                  # Category entity
│   │   │   ├── product.py                   # Product entity (price, stock_quantity)
│   │   │   ├── customer.py                  # Customer entity
│   │   │   └── sale.py                      # Sale + SaleItem entities
│   │   └── repositories/                    # Repository interfaces (ports)
│   ├── application/
│   │   ├── exceptions.py                    # ValidationError, NotFoundError, ConflictError, ...
│   │   └── use_cases/
│   │       ├── auth_use_cases.py            # Register (bootstrap-admin), Authenticate, CreateEmployee, UpdateEmployee
│   │       ├── category_use_cases.py        # Create/Update/Delete (guarded against categories still in use)
│   │       ├── product_use_cases.py         # CRUD + paginated/search listing
│   │       ├── customer_use_cases.py        # CRUD + paginated/search listing
│   │       ├── sale_use_cases.py            # CreateSaleUseCase = checkout logic; paginated listing
│   │       └── dashboard_use_cases.py       # Summary, top products, low stock, recent sales
│   ├── infrastructure/
│   │   ├── extensions.py                    # Shared SQLAlchemy instance
│   │   ├── models.py                        # ORM models: User/Category/Product/Customer/Sale/SaleItem
│   │   └── repositories/                    # SQLAlchemy implementations of each port
│   └── interfaces/
│       └── http/
│           ├── decorators.py                # @role_required(*roles)
│           ├── auth_routes.py               # /api/auth/*
│           ├── employee_routes.py           # /api/employees (admin only)
│           ├── category_routes.py           # /api/categories
│           ├── product_routes.py            # /api/products
│           ├── customer_routes.py           # /api/customers
│           ├── sale_routes.py               # /api/sales, /api/sales/checkout
│           └── dashboard_routes.py          # /api/dashboard/*
├── run.py                                    # Entry point: create_app().run()
├── login.sh                                  # Helper: log in from the shell, exports $TOKEN
├── postman-login-test.js                     # Postman "Tests" script for the login request
├── postman-refresh-test.js                   # Postman "Tests" script for the refresh request
├── .env.example                              # Copy to .env; set DATABASE_URL for Supabase
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.11 or later
- pip

### Installation

```bash
git clone https://github.com/macoskoemheang/CURD-RESTfull-API.git
cd CURD-RESTfull-API

python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Run (local SQLite — no setup needed)

```bash
python run.py
```

The API starts at **http://127.0.0.1:5000** and creates `pos.db` automatically on first run.

### First-time setup: create the admin account

The **very first** account registered becomes `admin` automatically. Every
account after that defaults to `cashier`.

```bash
curl -X POST http://127.0.0.1:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "owner", "password": "secret123"}'
```

## Roles & Permissions

| Action                              | Cashier | Admin |
|--------------------------------------|:-------:|:-----:|
| View products / categories           | ✅      | ✅    |
| Create / view customers              | ✅      | ✅    |
| Checkout a sale                      | ✅      | ✅    |
| View sales history                   | ✅      | ✅    |
| View dashboard / analytics           | ✅      | ✅    |
| Create / update / delete products    | ❌      | ✅    |
| Create / update / delete categories  | ❌      | ✅    |
| Manage employees (create/list/update)| ❌      | ✅    |

A cashier calling an admin-only endpoint gets `403 Forbidden`.

## API Documentation

Open **http://127.0.0.1:5000/** — it redirects straight to the interactive Swagger UI.

| Resource          | URL                                          |
|-------------------|-----------------------------------------------|
| Swagger UI        | `http://127.0.0.1:5000/apidocs/`              |
| Raw OpenAPI spec  | `http://127.0.0.1:5000/apispec_1.json`        |

Click **Authorize** in Swagger UI and paste `Bearer <your access_token>` to call protected endpoints directly from the browser.

## Authentication Flow

```
 1. POST /api/auth/register  →  create an account (first one becomes admin)
 2. POST /api/auth/login     →  get access_token + refresh_token (role is baked into the token)
 3. Attach "Authorization: Bearer <access_token>" to every request
 4. When the access token expires (15 min), POST /api/auth/refresh
    with "Authorization: Bearer <refresh_token>" to get a new one
```

## API Reference

### Auth

| Method | Endpoint             | Auth required  | Description                            |
|--------|-----------------------|----------------|------------------------------------------|
| POST   | `/api/auth/register`  | —              | Self-register (first account = admin)    |
| POST   | `/api/auth/login`     | —              | Log in, returns `access_token` + `refresh_token` |
| POST   | `/api/auth/refresh`   | Refresh token  | Exchange refresh token for a new access token |
| GET    | `/api/auth/me`        | Any            | Get the current logged-in user           |

### Employees *(admin only)*

| Method | Endpoint                 | Description                        |
|--------|---------------------------|--------------------------------------|
| GET    | `/api/employees`          | List all employees                   |
| POST   | `/api/employees`          | Create an employee with a specific role |
| GET    | `/api/employees/<id>`     | Get a single employee                |
| PUT    | `/api/employees/<id>`     | Update role and/or is_active (cannot target your own account) |

### Categories

Categories support **one level of subcategories** — set `parent_id` when
creating/updating to nest a category under an existing top-level one. A
subcategory cannot itself have subcategories. Names only need to be unique
among siblings (same `parent_id`), so a top-level category and a
subcategory can share a name.

| Method | Endpoint                 | Auth required | Description        |
|--------|---------------------------|---------------|----------------------|
| GET    | `/api/categories`          | Any           | List all categories (flat list, each with `parent_id`) |
| POST   | `/api/categories`          | Admin         | Create a category or subcategory (`{"name", "parent_id"?}`) |
| PUT    | `/api/categories/<id>`     | Admin         | Rename and/or reparent a category |
| DELETE | `/api/categories/<id>`     | Admin         | Delete a category (400 if it has subcategories or products still assigned) |

### Products

| Method | Endpoint                    | Auth required | Description        |
|--------|-------------------------------|---------------|----------------------|
| GET    | `/api/products`               | Any           | List products (paginated, `search`, `category_id`) |
| GET    | `/api/products/<id>`          | Any           | Get a single product |
| POST   | `/api/products`               | Admin         | Create a product (`category_id` may point to a top-level category or a subcategory) |
| PUT    | `/api/products/<id>`          | Admin         | Update a product (overwrites `stock_quantity` if provided) |
| POST   | `/api/products/<id>/stock`    | Admin         | **Restock**: adds `{"quantity"}` to the current stock (use this to receive inventory, rather than overwriting via PUT) |
| DELETE | `/api/products/<id>`          | Admin         | Delete a product (400 if it has existing sales) |

### Customers

| Method | Endpoint                 | Auth required | Description          |
|--------|---------------------------|---------------|------------------------|
| GET    | `/api/customers`           | Any           | List customers (paginated, `search`) |
| GET    | `/api/customers/<id>`      | Any           | Get a single customer  |
| POST   | `/api/customers`           | Any           | Create a customer      |
| PUT    | `/api/customers/<id>`      | Any           | Update a customer      |

### Sales

| Method | Endpoint                 | Auth required | Description                                  |
|--------|---------------------------|---------------|-------------------------------------------------|
| GET    | `/api/sales`               | Any           | List sales (paginated, `start_date`/`end_date`, newest first) |
| GET    | `/api/sales/<id>`          | Any           | Get a single sale                               |
| POST   | `/api/sales/checkout`      | Any           | Checkout a cart: creates a sale, decrements stock |

### Dashboard

| Method | Endpoint                        | Auth required | Description                                  |
|--------|-----------------------------------|---------------|-------------------------------------------------|
| GET    | `/api/dashboard/summary`          | Any           | Revenue, sale count, product/customer counts, low-stock count |
| GET    | `/api/dashboard/top-products`     | Any           | Best-selling products by quantity (`limit`)  |
| GET    | `/api/dashboard/low-stock`        | Any           | Products at/below a stock `threshold`        |
| GET    | `/api/dashboard/recent-sales`     | Any           | Most recent sales (`limit`)                  |

## Pagination & Filtering

`GET /api/products`, `/api/customers`, and `/api/sales` return a paginated
envelope instead of a bare array:

```json
{
  "items": [ ... ],
  "page": 1,
  "per_page": 20,
  "total": 137
}
```

Query params:

| Endpoint          | Params                                              |
|-------------------|-------------------------------------------------------|
| `/api/products`   | `page`, `per_page` (max 100), `search`, `category_id` |
| `/api/customers`  | `page`, `per_page` (max 100), `search`                |
| `/api/sales`      | `page`, `per_page` (max 100), `start_date`, `end_date` (ISO format, e.g. `2026-09-01`) |

## Dashboard / Analytics

Built specifically for a management dashboard/portal:

```bash
curl $BASE/api/dashboard/summary -H "Authorization: Bearer $TOKEN"
# {"total_revenue": 1234.5, "total_sales": 42, "total_products": 18, "total_customers": 9, "low_stock_count": 2}

curl "$BASE/api/dashboard/top-products?limit=3" -H "Authorization: Bearer $TOKEN"
curl "$BASE/api/dashboard/low-stock?threshold=5" -H "Authorization: Bearer $TOKEN"
curl "$BASE/api/dashboard/recent-sales?limit=10" -H "Authorization: Bearer $TOKEN"
```

## CORS (for a web portal)

CORS is enabled on all `/api/*` routes via `flask-cors`, so a separately
hosted frontend (e.g. React/Vue dashboard on `localhost:5173` or a deployed
domain) can call this API directly from the browser.

By default all origins are allowed (`CORS_ORIGINS=*`), which is fine for
local development. For a real deployment, restrict it in `.env`:

```
CORS_ORIGINS=https://my-pos-dashboard.com,http://localhost:5173
```

## Example Requests

```bash
BASE=http://127.0.0.1:5000

# 1. Register the first user -> becomes admin
curl -X POST $BASE/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "owner", "password": "secret123"}'

# 2. Login
LOGIN=$(curl -s -X POST $BASE/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "owner", "password": "secret123"}')
TOKEN=$(echo $LOGIN | python3 -c "import sys,json;print(json.load(sys.stdin)['access_token'])")

# 3. Create a category
curl -X POST $BASE/api/categories \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"name": "Drinks"}'

# 4. Create a product
curl -X POST $BASE/api/products \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"name": "Iced Coffee", "price": 2.50, "stock_quantity": 100, "category_id": 1}'

# 5. Create a customer
curl -X POST $BASE/api/customers \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "phone": "012345678"}'

# 6. Checkout a sale
curl -X POST $BASE/api/sales/checkout \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"customer_id": 1, "items": [{"product_id": 1, "quantity": 2}]}'

# 7. Create a cashier employee (admin only)
curl -X POST $BASE/api/employees \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"username": "cashier1", "password": "secret123", "role": "cashier"}'
```

Prefer a shell shortcut over copy-pasting tokens? Source [`login.sh`](login.sh):

```bash
source login.sh owner secret123
curl $BASE/api/products -H "Authorization: Bearer $TOKEN"
```

## Migrating to Supabase

By default the app uses local SQLite (`pos.db`). To point it at a real
Supabase Postgres database instead:

1. **Create a project** at [supabase.com](https://supabase.com) (free tier is fine).
2. In the Supabase dashboard, go to **Project Settings → Database → Connection string → URI**.
   Copy the connection string (use the **Session pooler** option — works well for a simple Flask app).
3. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
4. In `.env`, set `DATABASE_URL` to the string you copied, but change the
   scheme from `postgresql://` to `postgresql+psycopg://` (this project uses
   the psycopg3 driver):
   ```
   DATABASE_URL=postgresql+psycopg://postgres.xxxx:YOUR-PASSWORD@aws-0-xxxx.pooler.supabase.com:5432/postgres
   ```
5. Also set a real `JWT_SECRET_KEY` in `.env`.
6. Run the app as usual:
   ```bash
   python run.py
   ```
   `db.create_all()` will create all the POS tables (`users`, `categories`,
   `products`, `customers`, `sales`, `sale_items`) directly in your Supabase
   database on first run — no manual SQL needed.
7. Register your first user again against the new database — it becomes
   admin, since the Supabase `users` table starts empty.

No application code changes are needed to switch — only the `.env` file.

## Notes

- `JWT_SECRET_KEY` defaults to a dev value in `app/config.py`. Always set a
  real `JWT_SECRET_KEY` in `.env` before deploying anywhere real.
- Access tokens expire in 15 minutes, refresh tokens in 30 days
  (flask-jwt-extended defaults).
- Checkout (`POST /api/sales/checkout`) validates stock and rejects the
  whole sale with `400` if any item doesn't have enough stock — nothing is
  partially applied.
- This is a learning/demo project — the built-in Flask dev server is not
  intended for production traffic; use something like `gunicorn` behind a
  reverse proxy for real deployments.
- **Schema changes:** `db.create_all()` only creates tables that don't exist
  yet — it will **not** add new columns to a table that's already there
  (whether on SQLite or Supabase). If you add a field to a model after
  tables already exist, you need to add the column manually, e.g.:
  ```sql
  ALTER TABLE users ADD COLUMN IF NOT EXISTS new_column TEXT;
  ```
  For anything beyond occasional additive columns, consider adding
  `Flask-Migrate`/Alembic to manage schema changes properly.
- Deactivating an employee (`is_active: false`) blocks future logins, but an
  access token issued *before* deactivation stays valid until it expires
  (up to 15 minutes) — JWTs are stateless. For instant revocation you'd need
  a token blocklist, which isn't implemented here.
