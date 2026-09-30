# 🖥️ POS Shop Dashboard

A management dashboard for the [POS Shop API](../flask-rest-api) — built with **React**, **TypeScript**, and **Tailwind CSS**, structured in clean-architecture layers to mirror the backend.

![React](https://img.shields.io/badge/react-19-61dafb.svg)
![TypeScript](https://img.shields.io/badge/typescript-5-3178c6.svg)
![Vite](https://img.shields.io/badge/vite-7-646cff.svg)
![Tailwind](https://img.shields.io/badge/tailwind-4-06b6d4.svg)

## Features

- 🔐 JWT login/register, with automatic access-token refresh on 401
- 📊 Dashboard: revenue, sales, product/customer counts, top-products chart, low-stock alerts, recent sales
- 🛒 POS-style Checkout screen: click products to build a cart, then check out
- 📦 Products & Categories management (admin-only mutations), with one level of subcategories
- 📥 Restock: add units to a product's existing stock without a full edit
- 👥 Customers management
- 🧾 Sales history with date-range filtering
- 👤 Employee management: create staff, change roles, activate/deactivate (admin only)
- Role-aware UI — cashiers don't see admin-only actions or the Employees page

## Tech Stack

| Concern           | Library                     |
|--------------------|------------------------------|
| Framework          | React 19 + TypeScript        |
| Build tool         | Vite                         |
| Styling            | Tailwind CSS v4              |
| Routing            | React Router                 |
| Server state       | TanStack Query               |
| Client state       | Zustand (persisted to localStorage) |
| HTTP client        | Axios                        |
| Charts             | Recharts                     |
| Icons              | lucide-react                 |
| Notifications      | react-hot-toast              |

## Architecture

Layered to mirror the Flask backend's Clean Architecture:

```
src/
├── domain/types/         # TypeScript types mirroring backend DTOs (Product, Sale, User, ...)
├── api/                  # HTTP client + one module per resource (productApi, saleApi, ...)
├── application/
│   ├── hooks/            # TanStack Query hooks wrapping the api/ layer (useProducts, useCheckout, ...)
│   └── stores/           # Zustand auth store (tokens + current user)
├── presentation/
│   ├── components/
│   │   ├── ui/           # Reusable primitives: Button, Card, Table, Modal, Input, ...
│   │   └── layout/       # Sidebar, Topbar, DashboardLayout
│   ├── pages/            # One component per route
│   └── routes/           # ProtectedRoute / AdminRoute guards + route table
├── lib/                  # Formatters (currency, dates)
├── App.tsx               # Providers: QueryClient, Router, Toaster
└── main.tsx              # Entry point
```

- **`domain`** has no dependency on anything else — just types.
- **`api`** turns HTTP calls into typed promises; nothing here knows about React.
- **`application`** adapts `api` for React via TanStack Query and holds client-side auth state.
- **`presentation`** is pages/components; it only talks to `application` hooks, never `api` directly.

## Getting Started

### Prerequisites

- Node.js 18+
- The [Flask backend](../flask-rest-api) running (locally or against Supabase)

### Installation

```bash
cd web-front
npm install
```

### Configure the API URL

```bash
cp .env.example .env
```

By default it points at `http://127.0.0.1:5000/api`. Change `VITE_API_BASE_URL` in `.env` if your backend runs elsewhere.

### Run

```bash
npm run dev
```

Opens at **http://localhost:5173**. Make sure the backend is also running (`cd ../flask-rest-api && source venv/bin/activate && python run.py`) and that its CORS `CORS_ORIGINS` allows `http://localhost:5173` (default `*` already does).

### First login

Same as the backend: the first account you register becomes `admin`; everyone after that is a `cashier`. Use the **Register** tab on the login screen.

### Build for production

```bash
npm run build
```

Outputs to `dist/`. Serve it with any static host, and set `VITE_API_BASE_URL` at build time to point at your deployed backend.

## Notes

- Access tokens are held in memory/localStorage via Zustand; when the API returns `401`, the client transparently retries once after refreshing the token, then logs the user out if that also fails.
- Admin-only UI (product/category mutations, Employees page) is hidden client-side based on the JWT role claim — the backend independently enforces the same rules, so this is a UX convenience, not the security boundary.
