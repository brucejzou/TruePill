import flask
from flask import request, jsonify, abort
from src.bias import Bias, get_bias
from src.suggestions import get_suggested_articles
from src.url_helpers import is_facebook_url, extract_fb_url, is_twitter_url, extract_twitter_url
from config import Config
from tinydb import TinyDB
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)
app.config.from_object(Config)
app.config['MEDIA_BIAS_DB'] = TinyDB(app.config['BIAS_DB_PATH'])

@app.route('/api/truepill/', methods=['POST'])
def process_url():
    if not request.json or not 'article_url' in request.json:
        abort(500)

    article_url = request.json['article_url']
    num_suggestions = request.json['number_suggestions']

    if is_facebook_url(article_url):
        article_url = extract_fb_url(article_url)

    if is_twitter_url(article_url):
        article_url = extract_twitter_url(article_url)

    bias = get_bias(article_url, app.config['MEDIA_BIAS_DB'])
    if (num_suggestions > 0):
        suggested_articles = get_suggested_articles(article_url, app.config['NUM_SUGGESTIONS'], app.config)

        response = {
            'article_url': article_url,
            'bias': bias,
            'suggested_articles': suggested_articles
        }
    else:
        response = {
            'article_url': article_url,
            'bias': bias
        }

    return jsonify(response), 200

@app.after_request
def apply_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = "POST"
    response.headers['Access-Control-Allow-Headers'] = "Content-Type"
    return response

if __name__ == '__main__':
    app.run()
