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
    rv = client.post('/api/truepill/', data=None)
    assert rv.status_code == 500

def test_process_url_not_fb_url(client):
    rv = client.post('/api/truepill/', json={
        "article_url" : "https://www.bloomberg.com/graphics/2021-covid-race-and-recovery/?srnd=premium",
        "number_suggestions": 4
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
    rv = client.post('/api/truepill/', json={
        "article_url" : "https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.reuters.com%2Fnews%2Fpicture%2Fthai-shelter-for-disabled-stray-dogs-thr-idUSRTX8XTG1%2F1550403886%3Ffbclid%3DIwAR0Fd61ZalJYMVS8Cbq6KUgePJ937WGHxmRMQU59kNG4AxYzEc4fJ1t-ws8&amp;h=AT1MPSv84XaEV7uPMPwsnZ3AGE08Iz2UYdsTAVnd7v7aMC56WgCvnMuaVMVK4CxKePDN0RD7zwakpEFLYmeEsFM9S8_SuK3NsoFaDZQ61f3wtCNVwUBIAniqA8CJ20Uqb79B&amp;__tn__=H-R&amp;c[0]=AT0XhQ85FG3-3DpjwxheOyqDtDPDqzDW0CeEkdc1xZyiCgywoRCMZrnPFVhOhhgPpk4rg8IgPhbqV7clzcaoHmJ5TshCqxOoK9wzglMwUPcR_jSGI3ivJQmVElNj8XEfh4XKvwtDDx3CwD736f_CFcvxB8WbkkTbcKQaSrETNYCf0LvCWgvn_vTJ",
        "number_suggestions": 4
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
