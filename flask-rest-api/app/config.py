import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # Defaults to a local SQLite file. Set DATABASE_URL (in a .env file) to
    # point at Supabase/Postgres instead -- see README "Migrating to Supabase".
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///pos.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-secret-change-me")
    SWAGGER = {
        "title": "POS Shop API",
        "uiversion": 3,
    }

    # Comma-separated list of allowed origins for the web portal, e.g.
    # "https://my-pos-dashboard.com,http://localhost:5173". Defaults to "*"
    # (any origin) for local development.
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")
