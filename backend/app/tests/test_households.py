from app import create_app
import pytest

@pytest.fixture()
def auth_headers():
    # no real token during CI; just a placeholder
    return {"Authorization": "Bearer test"}

def test_get_households(auth_headers):
    app = create_app()
    client = app.test_client()
    res = client.get("/api/v1/households/", headers=auth_headers)
    # Smoke test: endpoint reachable and not a server error.
    assert res.status_code < 500
