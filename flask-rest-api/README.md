# 🗒️ Task Manager API

A RESTful Task Manager API built with **Flask**, **SQLAlchemy**, and **JWT authentication**, documented with an interactive **Swagger UI**.

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0-black.svg)
![JWT](https://img.shields.io/badge/auth-JWT-orange.svg)

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Documentation](#api-documentation)
- [Authentication Flow](#authentication-flow)
- [API Reference](#api-reference)
- [Example Requests](#example-requests)
- [Notes](#notes)

## Features

- 🔐 JWT-based authentication (access + refresh tokens)
- ✅ Full CRUD for tasks
- 👤 User registration, login, and user listing
- 📑 Interactive Swagger UI, generated from route docstrings
- 💾 SQLite persistence via SQLAlchemy — zero external DB setup

## Tech Stack

| Layer          | Technology              |
|----------------|--------------------------|
| Language       | Python 3.11+             |
| Framework      | Flask 3.0                |
| ORM            | Flask-SQLAlchemy         |
| Database       | SQLite                   |
| Auth           | Flask-JWT-Extended       |
| API Docs       | Flasgger (Swagger UI)    |

## Project Structure

```
flask-rest-api/
├── app.py                     # App factory, config, JWT + Swagger setup, entry point
├── auth.py                    # Auth blueprint: register, login, refresh, me, users
├── extensions.py               # Shared SQLAlchemy instance
├── models.py                   # User and Task models
├── routes.py                   # Task CRUD blueprint (JWT-protected)
├── login.sh                    # Helper: log in from the shell, exports $TOKEN
├── postman-login-test.js       # Postman "Tests" script for the login request
├── postman-refresh-test.js     # Postman "Tests" script for the refresh request
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

### Run

```bash
python app.py
```

The API starts at **http://127.0.0.1:5000** and creates `tasks.db` automatically on first run.

## API Documentation

Open **http://127.0.0.1:5000/** — it redirects straight to the interactive Swagger UI.

| Resource          | URL                                          |
|-------------------|-----------------------------------------------|
| Swagger UI        | `http://127.0.0.1:5000/apidocs/`              |
| Raw OpenAPI spec  | `http://127.0.0.1:5000/apispec_1.json`        |

Click **Authorize** in Swagger UI and paste `Bearer <your access_token>` to call protected endpoints directly from the browser.

## Authentication Flow

```
 1. POST /api/auth/register  →  create an account
 2. POST /api/auth/login     →  get access_token + refresh_token
 3. Attach "Authorization: Bearer <access_token>" to every /api/tasks request
 4. When the access token expires (15 min), POST /api/auth/refresh
    with "Authorization: Bearer <refresh_token>" to get a new one
```

## API Reference

### Auth

| Method | Endpoint             | Auth required  | Description                            |
|--------|----------------------|----------------|------------------------------------------|
| POST   | `/api/auth/register`  | —              | Create a new user                        |
| POST   | `/api/auth/login`     | —              | Log in, returns `access_token` + `refresh_token` |
| POST   | `/api/auth/refresh`   | Refresh token  | Exchange refresh token for a new access token |
| GET    | `/api/auth/me`        | Access token   | Get the current logged-in user           |
| GET    | `/api/auth/users`     | Access token   | List all registered users                |

### Tasks

*All task endpoints require `Authorization: Bearer <access_token>`.*

| Method | Endpoint             | Description        |
|--------|-----------------------|----------------------|
| GET    | `/api/tasks`           | List all tasks       |
| GET    | `/api/tasks/<id>`      | Get a single task    |
| POST   | `/api/tasks`           | Create a new task    |
| PUT    | `/api/tasks/<id>`      | Update a task        |
| DELETE | `/api/tasks/<id>`      | Delete a task        |

## Example Requests

```bash
BASE=http://127.0.0.1:5000

# Register
curl -X POST $BASE/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "secret123"}'

# Login (save the access_token from the response)
curl -X POST $BASE/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "secret123"}'

TOKEN="paste-your-access_token-here"

# Create a task
curl -X POST $BASE/api/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Flask", "description": "Build a REST API"}'

# List tasks
curl $BASE/api/tasks -H "Authorization: Bearer $TOKEN"

# Update a task
curl -X PUT $BASE/api/tasks/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"done": true}'

# Delete a task
curl -X DELETE $BASE/api/tasks/1 -H "Authorization: Bearer $TOKEN"

# Refresh the access token
curl -X POST $BASE/api/auth/refresh -H "Authorization: Bearer <refresh_token>"
```

Prefer a shell shortcut over copy-pasting tokens? Source [`login.sh`](login.sh):

```bash
source login.sh alice secret123
curl $BASE/api/tasks -H "Authorization: Bearer $TOKEN"
```

## Notes

- `JWT_SECRET_KEY` defaults to a dev value in `app.py`. Set the `JWT_SECRET_KEY` environment variable to a strong random value before deploying anywhere real.
- Access tokens expire in 15 minutes, refresh tokens in 30 days (flask-jwt-extended defaults).
- This is a learning/demo project — the built-in Flask dev server is not intended for production use.
