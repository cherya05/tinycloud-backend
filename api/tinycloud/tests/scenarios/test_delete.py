from datetime import datetime
from tinycloud.extensions import db
from tinycloud.models.url_mapping import UrlMapping

def test_delete_existing_short_code(client):
    url_mapping = UrlMapping(
        long_url="https://example.com",
        short_url="ABC12345",
        created_at=datetime.now(),
    )

    db.session.add(url_mapping)
    db.session.commit()

    response = client.delete(f"/url-mapping/{url_mapping.id}")

    assert response.status_code == 200
    body = response.get_json()
    assert body["message"] == "URL deleted successfully"


def test_delete_short_code_not_found(client):
    response = client.delete("/url-mapping/555")

    assert response.status_code == 404
    body = response.get_json()
    assert body["error"] == "URL not found"

def test_delete_removes_record(client):
    url_mapping = UrlMapping(
        long_url="https://example.com",
        short_url="ABC12345",
        created_at=datetime.now(),
    )
    db.session.add(url_mapping)
    db.session.commit()

    response = client.delete(f"/url-mapping/{url_mapping.id}")

    assert response.status_code == 200
    deleted_mapping = UrlMapping.query.filter_by(id=url_mapping.id).first()
    assert deleted_mapping is None