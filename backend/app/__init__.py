import re
import time
from flask import Flask
from .config import DevConfig
from flask_cors import CORS
from .extensions import db, jwt, migrate
from sqlalchemy.exc import OperationalError


def _register_bps(app):
    # === Blueprint registrations ===
    from .blueprints.health.routes import bp as health_bp
    from .blueprints.households.routes import bp as households_bp
    from .blueprints.pantry.routes import bp as pantry_bp
    from .blueprints.auth.routes import bp as auth_bp
    from .blueprints.items.routes import bp as items_bp
    from .blueprints.lists.routes import bp as lists_bp
    from .blueprints.foodref.routes import bp as foodref_bp

    app.register_blueprint(health_bp, url_prefix="/api/v1/health")
    app.register_blueprint(households_bp, url_prefix="/api/v1/households")
    app.register_blueprint(pantry_bp, url_prefix="/api/v1/pantry")
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(items_bp, url_prefix="/api/v1/items")
    app.register_blueprint(lists_bp, url_prefix="/api/v1/lists")
    app.register_blueprint(foodref_bp, url_prefix="/api/v1/foodref")


def create_app(config_class=DevConfig) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # === CORS setup ===
    # allow localhost dev ports, the main production host, and vercel preview subdomains
    CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [
                # local dev origins
                "http://localhost:5173",
                "http://localhost:5500",
                "http://localhost:3000",
                "http://127.0.0.1:5500",
                # production frontends
                "https://mygrocer.vercel.app",
                "https://mygrocer-backend.onrender.com",
                # regex to allow bracketed IPv6 preview & other localhost variants
                re.compile(r"^https?:\/\/(\[.*\]|localhost|127\.0\.0\.1)(:\d+)?$")
            ]
        }
    },
    supports_credentials=True,
)

    _register_bps(app)

    # === ONE-TIME: auto-create tables for free-tier deploy with retry ===
    for attempt in range(5):
        try:
            with app.app_context():
                db.create_all()
                print("✅ Database tables created successfully (auto-run).")
                break
        except OperationalError as e:
            print(f"⚠️ DB not ready, retrying ({attempt + 1}/5): {e}")
            time.sleep(5)
        except Exception as e:
            print(f"❌ Database setup failed: {e}")
            break

    # === Health Check ===
    @app.get("/api/v1/health")
    def health():
        return {"ok": True}, 200

    return app
