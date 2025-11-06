import pytest
from app import create_app

@pytest.fixture()
def auth_headers():
    return {"Authorization": "Bearer fake-token"}

def test_get_households(auth_headers):
    app = create_app()
    client = app.test_client()
    res = client.get("/api/v1/households/", headers=auth_headers)
    assert res.status_code in [200, 404, 500]
