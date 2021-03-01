import random
from bias import Bias, get_bias
from news_search import google_news_search
from rake_nltk import Rake
from bs4 import BeautifulSoup
from bs4.element import Comment
import requests

TEXT_LENGTH_FILTER = 80

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

    article_text, article_date = get_article_text(article_url)
    article_keywords = get_article_keywords(article_text)
    related_articles = get_related_articles(article_keywords, article_date, num_suggestions, trusted_sources, top_n_keywords, date_margin, app_config['MEDIA_BIAS_DB'])

    # add biases
    suggested_articles = []
    for article in related_articles:
        bias = get_bias(article, app_config['MEDIA_BIAS_DB'])
        suggestion = {'bias': bias, 'article_url': article}
        suggested_articles.append(suggestion)

    return suggested_articles 

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    if len(str(element)) < TEXT_LENGTH_FILTER:
        return False
    return True

def get_article_text(article_url):
    """
    Gets the article text from the given article url as a string.

    Arguments
    ----------
    article_url: (string), the url of the original article.
    """
    result = requests.get(article_url)

    if result.status_code == 200:
        content = result.content
        soup = BeautifulSoup(content, features='html.parser')
        texts = soup.find_all(text=True)
        visible_texts = filter(tag_visible, texts)
        return u" ".join(t.strip() for t in visible_texts)

def get_article_keywords(article_text):
    """
    Gets the keywords or phrases of the article returned as a list of strings.

    Arguments
    ----------
    article_text: (string), string containing the text of the article.
    """

    r = Rake()
    r.extract_keywords_from_text(article_text)

    return r.get_ranked_phrases()

def get_related_articles(article_keywords, article_date, num_suggestions, trusted_sources, top_n_keywords, date_margin, bias_db):
    """
    Gets a list of related articles (url) (length = num_suggestions) from trusted sources based on the article keywords.

    Arguments
    ----------
    article_keywords: ([string]), list of keywords defining the article.
    num_suggestions: (int), number of related articles to find.
    trusted_sources: ([string]), list of trusted news sources to find related articles from.
    top_n_keywords: (int), number of keywords to keep.
    date_margin: (int), number of days to +- from the article date for searching.
    """
    suggested_articles = []
    chosen_sources = []

    if trusted_sources:
        if num_suggestions > len(trusted_sources): # wants more suggestions than trusted sources, just return from all sources
            num_suggestions = len(trusted_sources)
        chosen_sources = random.sample(trusted_sources, num_suggestions) # randomly choose some sources

    selected_keywords = article_keywords[:top_n_keywords] # Get the top_n_keywords to search with
    related_articles = google_news_search(selected_keywords, article_date, num_suggestions, chosen_sources, date_margin, bias_db)

    return related_articles

