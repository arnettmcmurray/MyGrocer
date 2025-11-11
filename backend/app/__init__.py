from flask import Flask
from .config import DevConfig
from flask_cors import CORS
from .extensions import db, jwt, migrate


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
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": [
                    "http://localhost:5173",
                    "https://mygrocer.vercel.app",
                    "https://mygrocer-backend.onrender.com",
                ]
            }
        },
        supports_credentials=True,
    )

    _register_bps(app)

    return app
