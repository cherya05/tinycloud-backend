from datetime import datetime
from tinycloud.extensions import db
from tinycloud.models.url_mapping import UrlMapping

def test_get_existing_short_code(client):
    url_mapping = UrlMapping(
        long_url="https://example.com",
        short_url="ABC12345",
        created_at=datetime.now(),
    )

    db.session.add(url_mapping)
    db.session.commit()

    response = client.get(f"/url-mapping/id/{url_mapping.id}")

    assert response.status_code == 200

    body = response.get_json()

    assert body["id"] == url_mapping.id
    assert body["long_url"] == "https://example.com"
    assert body["short_url"] == "ABC12345"

def test_short_code_not_found(client):
    response = client.get("/url-mapping/id/555")

    assert response.status_code == 404
    body = response.get_json()
    assert body["error"] == "URL not found"