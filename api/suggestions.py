import random
from bias import Bias, get_bias
from news_search import google_news_search

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


def get_article_text(article_url):
    """
    Gets the article text from the given article url as a string.

    Arguments
    ----------
    article_url: (string), the url of the original article.
    """

    return ""


def get_article_keywords(article_text):
    """
    Gets the keywords or phrases of the article returned as a list of strings.

    Arguments
    ----------
    article_text: (string), string containing the text of the article.
    """

    return []

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

