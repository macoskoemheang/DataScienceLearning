# Flask REST API — Task Manager

A RESTful API built with Flask and SQLAlchemy (SQLite) that manages a list
of tasks (CRUD), protected by JWT authentication.

## Setup

```bash
cd flask-rest-api
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

The API runs at `http://127.0.0.1:5000`.

## API Docs (Swagger)

Interactive Swagger UI: **http://127.0.0.1:5000/apidocs/**
Raw OpenAPI spec: `http://127.0.0.1:5000/apispec_1.json`

Click **Authorize** in Swagger UI and paste `Bearer <your access_token>` to
call the protected task endpoints from the browser.

## Auth Endpoints

| Method | Endpoint            | Auth required | Description                        |
|--------|---------------------|----------------|-------------------------------------|
| POST   | /api/auth/register  | No             | Create a new user                   |
| POST   | /api/auth/login     | No             | Log in, returns access + refresh    |
| POST   | /api/auth/refresh   | Refresh token  | Exchange refresh token for new access |
| GET    | /api/auth/me        | Access token   | Get the current logged-in user      |
| GET    | /api/auth/users     | Access token   | List all registered users            |

## Task Endpoints (all require a valid access token)

| Method | Endpoint             | Description         |
|--------|-----------------------|----------------------|
| GET    | /api/tasks             | List all tasks       |
| GET    | /api/tasks/<id>        | Get a single task    |
| POST   | /api/tasks             | Create a new task    |
| PUT    | /api/tasks/<id>        | Update a task        |
| DELETE | /api/tasks/<id>        | Delete a task        |

## Example requests (curl)

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

## Project Structure

```
flask-rest-api/
├── app.py           # App factory, config, JWT + Swagger setup, entry point
├── auth.py          # Auth blueprint: register, login, refresh, me
├── extensions.py    # SQLAlchemy instance
├── models.py        # User and Task models
├── routes.py        # Task CRUD blueprint (JWT-protected)
├── requirements.txt
└── README.md
```

## Notes

- `JWT_SECRET_KEY` defaults to a dev value in `app.py`. Set the
  `JWT_SECRET_KEY` environment variable to a strong random value in any
  real deployment.
- Access tokens expire in 15 minutes and refresh tokens in 30 days
  (flask-jwt-extended defaults). Use `/api/auth/refresh` to get a new
  access token without logging in again.
