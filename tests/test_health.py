def test_health(api_client):
    req = api_client.get("/health")
    assert req.ok
