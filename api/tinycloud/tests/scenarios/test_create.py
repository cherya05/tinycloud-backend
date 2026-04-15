from tinycloud.extensions import db
from tinycloud.models.url_mapping import UrlMapping
from tinycloud.routes import url_mapping

def test_create_short_code(client):
    response = client.post(
        "/url-mapping/",
        json={"long_url": "https://example.com"},
    )

    assert response.status_code == 201
    body = response.get_json()
    assert body["long_url"] == "https://example.com"
    assert len(body["short_url"]) == 8

def test_missing_long_url(client):
    response = client.post(
        "/url-mapping/",
        json={},
    )
    assert response.status_code == 400
    body = response.get_json()
    assert body["error"] == "Missing long_url field"

def test_invalid_json(client):
    response = client.post(
        "/url-mapping/",
        data="not-json",
        content_type="application/json",
    )
    assert response.status_code == 400
    body = response.get_json()
    assert body["error"] == "Invalid JSON data"

def test_retries_on_conflict(client, monkeypatch):
    existing_mapping = UrlMapping(
        long_url="https://existing.example.com",
        short_url="AAA111BB",
        created_at=url_mapping.datetime.now()
    )
    db.session.add(existing_mapping)
    db.session.commit()

    generated_codes = iter(["AAA111BB", "CCC222DD"])

    monkeypatch.setattr(
        url_mapping,
        "generate_short_code",
        lambda: next(generated_codes),
    )

    response = client.post(
        "/url-mapping/",
        json={"long_url": "https://one.example.com"},
    )

    assert response.status_code == 201
    body = response.get_json()
    assert body["short_url"] == "CCC222DD"
    assert body["long_url"] == "https://one.example.com"