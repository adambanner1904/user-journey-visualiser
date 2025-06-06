from app import db
from .fixtures import test_app, test_client

def test_create_app(test_app):
    assert "SQLALCHEMY_DATABASE_URI" in test_app.config
    assert test_app.config["SQLALCHEMY_DATABASE_URI"] == 'sqlite:///test.db'

    for table in ('project', 'service', 'endpoint', 'link', 'journey'):
        assert table in db.metadata.tables.keys()

def test_index_route(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'Digital Journey Creator and Explorer' in response.data
    assert b'My Projects' in response.data



