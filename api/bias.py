import urllib.parse
import tldextract
from enum import Enum
from tinydb import Query

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


def get_base_url(article_url):
    """
    Takes the article url and returns the base url.
    
    Example:
    Input: https://www.cnn.com/2021/02/06/us/ben-montgomery-shot-moonlight-book-trnd/index.html
    Output: https://www.cnn.com/

    """
    u = urllib.parse.urlparse(article_url)
    return u[0] + "://" + u[1] + '/'
    
def extract_fb_url(fb_url):
    """
    Takes a link from Facebook and converts it to the real url.

    Example:
    Input: https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.reuters.com%2Fnews%2Fpicture%2Fthai-shelter-for-disabled-stray-dogs-thr-idUSRTX8XTG1%2F1550403886%3Ffbclid%3DIwAR0Fd61ZalJYMVS8Cbq6KUgePJ937WGHxmRMQU59kNG4AxYzEc4fJ1t-ws8&amp;h=AT1MPSv84XaEV7uPMPwsnZ3AGE08Iz2UYdsTAVnd7v7aMC56WgCvnMuaVMVK4CxKePDN0RD7zwakpEFLYmeEsFM9S8_SuK3NsoFaDZQ61f3wtCNVwUBIAniqA8CJ20Uqb79B&amp;__tn__=H-R&amp;c[0]=AT0XhQ85FG3-3DpjwxheOyqDtDPDqzDW0CeEkdc1xZyiCgywoRCMZrnPFVhOhhgPpk4rg8IgPhbqV7clzcaoHmJ5TshCqxOoK9wzglMwUPcR_jSGI3ivJQmVElNj8XEfh4XKvwtDDx3CwD736f_CFcvxB8WbkkTbcKQaSrETNYCf0LvCWgvn_vTJ
    Output: https://www.reuters.com/news/picture/thai-shelter-for-disabled-stray-dogs-thr-idUSRTX8XTG1/1550403886?fbclid=IwAR0Fd61ZalJYMVS8Cbq6KUgePJ937WGHxmRMQU59kNG4AxYzEc4fJ1t-ws8&h=AT1MPSv84XaEV7uPMPwsnZ3AGE08Iz2UYdsTAVnd7v7aMC56WgCvnMuaVMVK4CxKePDN0RD7zwakpEFLYmeEsFM9S8_SuK3NsoFaDZQ61f3wtCNVwUBIAniqA8CJ20Uqb79B&__tn__=H-R&c[0]=AT0XhQ85FG3-3DpjwxheOyqDtDPDqzDW0CeEkdc1xZyiCgywoRCMZrnPFVhOhhgPpk4rg8IgPhbqV7clzcaoHmJ5TshCqxOoK9wzglMwUPcR_jSGI3ivJQmVElNj8XEfh4XKvwtDDx3CwD736f_CFcvxB8WbkkTbcKQaSrETNYCf0LvCWgvn_vTJ

    """
    fb_url = fb_url[fb_url.index('l.php?u=') + 8: len(fb_url)]; 
    return urllib.parse.unquote(fb_url)

