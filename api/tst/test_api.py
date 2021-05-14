import os
import pytest
from src.api import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_process_url_no_article_url(client):
    rv = client.post('/api/truepill/', json={})
    assert rv.status_code == 500

def test_process_url_not_request_json(client):
    # chloe
    pass

def test_process_url_not_fb_url(client):
    pass

def test_process_url_fb_url(client):
    # chloe
    pass
