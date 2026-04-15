from datetime import datetime
from tinycloud.extensions import db
from tinycloud.models.url_mapping import UrlMapping

def test_update_existing_short_code(client):
    url_mapping = UrlMapping(
        long_url="https://example.com",
        short_url="ABC12345",
        created_at=datetime.now(),
    )
    
    db.session.add(url_mapping)
    db.session.commit()

    response = client.put(
        f"/url-mapping/{url_mapping.id}",
        json={"long_url": "https://updated.example.com"},
    )

    assert response.status_code == 200
    body = response.get_json()
    assert body["id"] == url_mapping.id
    assert body["long_url"] == "https://updated.example.com"
    assert body["short_url"] == "ABC12345"

def test_update_short_code_not_found(client):
    response = client.put(
        "/url-mapping/555",
        json={"long_url": "https://updated.example.com"}
    )

    assert response.status_code == 404

    body = response.get_json()
    assert body["error"] == "URL not found"

def test_update_missing_long_url(client):
    url_mapping = UrlMapping(
        long_url="https://example.com",
        short_url="ABC12345",
        created_at=datetime.now(),
    )

    db.session.add(url_mapping)
    db.session.commit()

    response = client.put(
        f"/url-mapping/{url_mapping.id}",
        json={},
    )

    assert response.status_code == 400

    body = response.get_json()
    assert body["error"] == "Missing long_url field"