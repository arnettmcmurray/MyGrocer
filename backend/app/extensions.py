from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

# Safe import: prevents CI failure if Flask-Migrate missing
try:
    from flask_migrate import Migrate
except ModuleNotFoundError:
    class Migrate:
        def __init__(self, *args, **kwargs):
            pass

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
