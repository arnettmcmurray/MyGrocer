import os

INSTANCE_DIR = os.path.join(os.path.dirname(__file__), "..", "instance")

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev")

class DevConfig(Config):
    DATABASE_URL = os.getenv("DATABASE_URL", "")
    if DATABASE_URL:
        uri = DATABASE_URL
        # normalize to psycopg2 driver
        if uri.startswith("postgres://"):
            uri = uri.replace("postgres://", "postgresql://")
        # Render requires sslmode=require
        if "?sslmode=require" not in uri:
            uri += "?sslmode=require"
        SQLALCHEMY_DATABASE_URI = uri
    else:
        os.makedirs(INSTANCE_DIR, exist_ok=True)
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(INSTANCE_DIR, 'mygrocer.db')}"
