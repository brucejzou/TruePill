import flask
from flask import request, jsonify, abort
from .bias import Bias, get_bias
from .suggestions import get_suggested_articles
from .url_helpers import is_facebook_url, extract_fb_url
from .config import Config
from tinydb import TinyDB
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)
app.config.from_object(Config)
app.config['MEDIA_BIAS_DB'] = TinyDB(app.config['BIAS_DB_PATH'])

@app.route('/api/truepill/', methods=['POST'])
def process_url():
    if not request.json or not 'article_url' in request.json:
        print(request.json)
        abort(500)

    article_url = request.json['article_url']
    num_suggestions = request.json.get('number_suggestions', app.config['NUM_SUGGESTIONS'])
    if is_facebook_url(article_url):
        article_url = extract_fb_url(article_url)
    bias = get_bias(article_url, app.config['MEDIA_BIAS_DB'])
    suggested_articles = get_suggested_articles(article_url, num_suggestions)

    response = {
        'article_url': article_url,
        'bias': bias,
        'suggested_articles': suggested_articles
    }

    return jsonify(response), 200

@app.after_request
def apply_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = "GET,POST,PUT,DELETE,OPTIONS"
    response.headers['Access-Control-Allow-Headers'] = "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    return response

if __name__ == '__main__':
    app.run()
