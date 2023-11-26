import json

def test_document_upload(auth_header, api_client):
    body = """
---
relay-filename: example.md
relay-to:
 - mytopic@myteam
---

Example text
"""
    req = api_client.post("/v1/doc", headers=auth_header, data=body)
    assert req.ok, req.text

    ret = req.json()
    doc_id = ret["result"]["relay_document"]

    req = api_client.get(f"/v1/doc/{doc_id}", headers=auth_header)
    assert req.ok, req.text

    ret = req.json()["result"]
    assert ret["body"] == body
    assert ret["relay-document"] == doc_id
    assert ret["relay-to"] == ["mytopic@myteam"]
    assert ret["relay-filename"] == "example.md"

    req = api_client.get(f"/v1/doc/{doc_id}", headers={**auth_header,
                         "content-type":"text/markdown"})
    assert req.ok, req.text

    assert req.text.startswith("""
---
relay-filename: example.md
relay-to:
 - mytopic@myteam
---
""")

    assert req.headers.get("x-relay-filename") == "example.md"
    assert req.headers.get("x-relay-document") == doc_id
    assert json.loads(req.headers.get("x-relay-to")) == ["mytopic@myteam"]
