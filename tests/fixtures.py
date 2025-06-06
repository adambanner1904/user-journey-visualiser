import pytest
from app import create_app

@pytest.fixture
def test_app():
    app = create_app('testing')
    return app

@pytest.fixture
def test_client(test_app):
    with test_app.test_client() as client:
        yield client

def clear_data(db):
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()