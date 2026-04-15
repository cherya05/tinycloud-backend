import pytest
from tinycloud.app import create_app
from tinycloud.extensions import db
from tinycloud.config import TestConfig

@pytest.fixture
def app():
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()
        yield app
        
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()