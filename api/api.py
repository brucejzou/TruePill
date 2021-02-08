import flask
from flask import request, jsonify
from bias import Bias, get_bias
from suggestions import get_suggested_articles
from url_helpers import is_facebook_url, extract_fb_url
from config import Config
from tinydb import TinyDB

app = flask.Flask(__name__)
app.config.from_object(Config)
app.config['MEDIA_BIAS_DB'] = TinyDB(app.config['BIAS_DB_PATH'])

@app.route('/api/truepill/', methods=['POST'])
def process_url():
    if not request.json or not 'article_url' in request.json:
        abort(400)

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

if __name__ == '__main__':
    app.run()