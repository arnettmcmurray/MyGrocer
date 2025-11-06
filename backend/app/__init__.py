from flask import Flask
from .config import DevConfig
from .extensions import db, jwt, migrate
from flask_cors import CORS

def _register_bps(app):
    from .blueprints.health.routes import bp as health_bp
    from .blueprints.households.routes import bp as households_bp
    from .blueprints.pantry.routes import bp as pantry_bp

    app.register_blueprint(health_bp, url_prefix="/api/v1/health")
    app.register_blueprint(households_bp, url_prefix="/api/v1/households")
    app.register_blueprint(pantry_bp, url_prefix="/api/v1/pantry")

def create_app(config_class=DevConfig) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

    _register_bps(app)
    return app
