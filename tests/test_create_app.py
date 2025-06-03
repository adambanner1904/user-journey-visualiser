import pytest
from app import create_app

@pytest.fixture
def app():
    app = create_app('testing')
    return app

@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client

def test_app_config(app):
    assert "SQLALCHEMY_DATABASE_URI" in app.config
    assert app.config["SQLALCHEMY_DATABASE_URI"] == 'sqlite:///:memory:'

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Journey Creator' in response.data
    assert b'Journey Explorer' in response.data