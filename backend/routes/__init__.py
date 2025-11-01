from flask import Flask
from backend.routes.auth import auth_bp
from backend.routes.users import users_bp
from backend.routes.lists import lists_bp
from backend.routes.items import items_bp
from backend.routes.recipes import recipes_bp
from backend.routes.planner import planner_bp
from backend.routes.grocery import grocery_bp
from backend.routes.health import health_bp

def register_blueprints(app: Flask) -> None:
    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(lists_bp, url_prefix="/api/lists")
    app.register_blueprint(items_bp, url_prefix="/api/items")
    app.register_blueprint(recipes_bp, url_prefix="/api/recipes")
    app.register_blueprint(planner_bp, url_prefix="/api/plan")
    app.register_blueprint(grocery_bp, url_prefix="/api/grocery")
