from flask import Flask
from backend.config import Config, init_extensions
from backend.routes import register_blueprints

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    init_extensions(app)
    register_blueprints(app)
    return app

if __name__ == "__main__":
    app = create_app()
    from backend.extensions import db
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=5001)
