import os
from datetime import timedelta
from dotenv import load_dotenv
from flask_cors import CORS
from backend.extensions import db, migrate, jwt, limiter

load_dotenv()

class Config:
    PROJECT_NAME = os.getenv("PROJECT_NAME", "MyGrocer")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///mygrocer.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-insecure-change")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.getenv("JWT_ACCESS_MIN", "30")))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.getenv("JWT_REFRESH_DAYS", "7")))

    CORS_ORIGINS = os.getenv("FRONTEND_URL", "*")

def init_extensions(app):
    CORS(app, resources={r"/api/*": {"origins": Config.CORS_ORIGINS}})
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    limiter.init_app(app)
