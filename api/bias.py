from enum import Enum

class Bias(Enum):
    LEFT = 1
    LEFT_CENTER = 2
    CENTER = 3
    RIGHT_CENTER = 4
    RIGHT = 5
    MIXED = 6

def get_bias(article_url, bias_db):
    """
    Gets the political bias of the news outlet that the given article is from.

    Arguments
    ----------
    article_url: (string), the url of the article.
    bias_db: (pickleDB), media bias pickleDB database.
    """

    base_url = get_base_url(article_url)

    return Bias.LEFT.name


def get_base_url(article_url):
    """
    Takes the article url and returns the base url.
    
    Example:
    Input: https://www.cnn.com/2021/02/06/us/ben-montgomery-shot-moonlight-book-trnd/index.html
    Output: https://www.cnn.com/

    """
    pass