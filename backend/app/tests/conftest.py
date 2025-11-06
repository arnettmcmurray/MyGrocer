import pytest
from backend.app import create_app
from backend.app.extensions import db


@pytest.fixture(scope="session")
def app():
    """Create and configure a new app instance for tests."""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "JWT_SECRET_KEY": "test-secret"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    """Return a Flask test client."""
    return app.test_client()


@pytest.fixture()
def auth_headers():
    """Dummy auth headers placeholder."""
    return {"Authorization": "Bearer fake-token"}
