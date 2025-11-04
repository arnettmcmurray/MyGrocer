from app import create_app

def test_health_route():
    app = create_app()
    client = app.test_client()
    res = client.get("/api/v1/health/")
    assert res.status_code == 200
    assert b'"status":"ok"' in res.data
