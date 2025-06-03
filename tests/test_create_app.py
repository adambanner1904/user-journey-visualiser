import pytest
from app import create_app, create_db, db

@pytest.fixture
def test_app():
    app = create_app('testing')
    return app

@pytest.fixture
def test_client(test_app):
    with test_app.test_client() as client:
        yield client

def test_create_app(test_app):
    assert "SQLALCHEMY_DATABASE_URI" in test_app.config
    assert test_app.config["SQLALCHEMY_DATABASE_URI"] == 'sqlite:///:memory:'

    for table in ('project', 'service', 'endpoint', 'link', 'journey'):
        assert table in db.metadata.tables.keys()

def test_index_route(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'Journey Creator' in response.data
    assert b'Journey Explorer' in response.data



