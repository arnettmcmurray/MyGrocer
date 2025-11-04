def test_get_households(client, auth_headers):
    resp = client.get("/api/v1/households/", headers=auth_headers)
    assert resp.status_code == 200
