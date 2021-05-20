import urllib.parse
import tldextract
from enum import Enum
from tinydb import Query
from src.url_helpers import get_base_url

class Bias(Enum):
    LEFT = 1
    LEFT_CENTER = 2
    CENTER = 3
    RIGHT_CENTER = 4
    RIGHT = 5
    UNKNOWN = 6

def get_bias(article_url, bias_db):
    """
    Gets the political bias of the news outlet that the given article is from.

    Arguments
    ----------
    article_url: (string), the url of the article.
    bias_db: (tinydb), media bias tinyDB database.
    """

    base_url = get_base_url(article_url)
    domain_name = tldextract.extract(base_url).domain

    Media = Query()
    query_results = bias_db.search( (Media.url == base_url) | (Media.domain_name == domain_name)) # domain_name backup lookup
    if query_results:
        first_res = query_results[0]
        return first_res['bias']

    return Bias.UNKNOWN.name
