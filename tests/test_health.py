# -*- coding: utf-8 -*-
def test_health(api_client):
    req = api_client.get("/health")
    req.raise_for_status()
