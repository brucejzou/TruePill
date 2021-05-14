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
    rv = client.post('/api/truepill/', json={
    "article_url" : "https://www.bloomberg.com/graphics/2021-covid-race-and-recovery/?srnd=premium"
    })
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert 'article_url' in json_data and json_data['article_url'] is not None, "article_url not in response"
    assert 'bias' in json_data and json_data['bias'] is not None, "bias not in response"
    assert 'suggested_articles' in json_data, "suggested_articles not in response"
    suggestions = json_data['suggested_articles']
    assert len(suggestions) >= 1, "no suggestions in response"
    first_suggestion = suggestions[0]
    assert 'article_title' in first_suggestion and first_suggestion['article_title'] is not None, 'article_title not in suggested article data'
    assert 'article_url' in first_suggestion and first_suggestion['article_url'] is not None, 'article_url not in suggested article data'
    assert 'bias' in first_suggestion and first_suggestion['bias'] is not None, 'bias not in suggested article data'
    

def test_process_url_fb_url(client):
    # chloe
    pass
