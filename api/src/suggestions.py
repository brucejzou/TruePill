import random
import datefinder
import articleDateExtractor
import string
from src.bias import Bias, get_bias
from src.news_search import google_news_search
from src.make_requests import make_request, get_random_header
from src.url_helpers import get_url_words
from goose3 import Goose
from cleantext import clean
from dateutil import parser
from rake_nltk import Metric, Rake
from bs4 import BeautifulSoup
from bs4.element import Comment

GOOGLE_CACHE_BASE_URL = "https://webcache.googleusercontent.com/search?q=cache:"

def get_suggested_articles(article_url, num_suggestions, app_config):
    """
    Gets a list of articles related to the given article.

    Arguments
    ----------
    article_url: (string), the url of the original article.
    num_suggestions: (int), the number of related articles to find.
    app_config: (flask app.config), used to get other config variables.
    """
    trusted_sources = app_config['TRUSTED_SOURCES']
    top_n_keywords = app_config['TOP_N_KEYWORDS']
    date_margin = app_config['DATE_MARGIN']
    url_match_threshold = app_config['URL_MATCH_THRESHOLD']


    article_text, article_date, article_url = get_article_text_and_date(article_url)

    if not url_words_match_text(article_url, article_text, url_match_threshold):
        gc_article_text, gc_article_date, gc_article_url = get_article_text_and_date(get_google_cache_url(article_url))
        if "error 404" not in gc_article_text.lower():
            article_text, article_date, article_url = gc_article_text, gc_article_date, gc_article_url

    article_keywords = get_article_keywords(article_text)
    related_articles = get_related_articles(article_url, article_keywords, article_date, num_suggestions, trusted_sources, top_n_keywords, date_margin, app_config['MEDIA_BIAS_DB'])

    # add biases
    suggested_articles = []
    chosen_bias = []

    for article in related_articles:
        bias = get_bias(article[1], app_config['MEDIA_BIAS_DB'])
        suggestion = {'bias': bias, 'article_url': article[1], 'article_title': article[0]}
        suggested_articles.append(suggestion)

    return suggested_articles

def get_google_cache_url(original_url):
    return GOOGLE_CACHE_BASE_URL + original_url

def url_words_match_text(article_url, article_text, threshold):
    url_words = get_url_words(article_url)
    if len(url_words) == 0:
        return True
    count = 0
    for word in url_words:
        if word in article_text:
            count += 1
    return count / len(url_words) >= threshold

def get_article_text_and_date(article_url):
    g = Goose({'http_headers': get_random_header()})
    article = g.extract(url=article_url)
    title = article.title
    body = clean(article.cleaned_text, no_line_breaks=True, no_punct=True)
    date = parser.parse(article.publish_date) if article.publish_date else None
    text = clean(title, no_punct=True) + body

    return text, date, article.canonical_link

def get_article_keywords(article_text):
    """
    Gets the keywords or phrases of the article returned as a list of strings.

    Arguments
    ----------
    article_text: (string), string containing the text of the article.
    """

    r = Rake(ranking_metric=Metric.WORD_FREQUENCY, min_length=1, max_length=4)
    r.extract_keywords_from_text(article_text)

    return r.get_ranked_phrases()

def get_related_articles(article_url, article_keywords, article_date, num_suggestions, trusted_sources, top_n_keywords, date_margin, bias_db):
    """
    Gets a list of related articles (url) (length = num_suggestions) from trusted sources based on the article keywords.

    Arguments
    ----------
    article_url: (string), url of the original articl
    article_keywords: ([string]), list of keywords defining the article.
    article_date: (datetime), date to search around. (Can be none)
    num_suggestions: (int), number of related articles to find.
    trusted_sources: ([string]), list of trusted news sources to find related articles from.
    top_n_keywords: (int), number of keywords to keep.
    date_margin: (int), number of days to +- from the article date for searching.
    bias_db: (TinyDB), media bias db.
    """
    suggested_articles = []
    chosen_sources = []

    if trusted_sources:
        if num_suggestions > len(trusted_sources): # wants more suggestions than trusted sources, just return from all sources
            num_suggestions = len(trusted_sources)

        chosen_sources = random.sample(trusted_sources, num_suggestions) # randomly choose some sources

    selected_keywords = article_keywords[:top_n_keywords] # Get the top_n_keywords to search with
    related_articles = google_news_search(article_url, selected_keywords, article_date, num_suggestions, chosen_sources, date_margin, bias_db)

    return related_articles
