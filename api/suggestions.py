
def get_suggested_articles(article_url, num_suggestions, trusted_sources):
    """
    Gets a list of articles related to the given article.

    Arguments
    ----------
    article_url: (string), the url of the original article.
    num_suggestions: (int), the number of related articles to find.
    """
    article_text = get_article_text(article_url)
    article_keywords = get_article_keywords(article_text)
    related_articles = get_related_articles(article_keywords, num_suggestions, trusted_sources)
    
    return [] 

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

def get_related_articles(article_keywords, num_suggestions, trusted_sources):
    """
    Gets a list of related articles (length = num_suggestions) from trusted sources based on the article keywords.

    Arguments
    ----------
    article_keywords: ([string]), list of keywords defining the article.
    num_suggestions: (int), number of related articles to find.
    trusted_sources: ([string]), list of trusted news sources to find related articles from.
    """

    return []
