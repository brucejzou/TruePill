import urllib.parse
import tldextract
import requests

def get_base_url(article_url):
    """
    Takes the article url and returns the base url.
    
    Example:
    Input: https://www.cnn.com/2021/02/06/us/ben-montgomery-shot-moonlight-book-trnd/index.html
    Output: https://www.cnn.com/

    """
    r = requests.get(article_url)
    u = urllib.parse.urlparse(r.url)
    return u[0] + "://" + u[1] + '/'

def is_facebook_url(url):
    tlde = tldextract.extract(url)
    return tlde.subdomain == 'l' and tlde.domain == 'facebook'

def extract_fb_url(fb_url):
    """
    Takes a link from Facebook and converts it to the real url.

    Example:
    Input: https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.reuters.com%2Fnews%2Fpicture%2Fthai-shelter-for-disabled-stray-dogs-thr-idUSRTX8XTG1%2F1550403886%3Ffbclid%3DIwAR0Fd61ZalJYMVS8Cbq6KUgePJ937WGHxmRMQU59kNG4AxYzEc4fJ1t-ws8&amp;h=AT1MPSv84XaEV7uPMPwsnZ3AGE08Iz2UYdsTAVnd7v7aMC56WgCvnMuaVMVK4CxKePDN0RD7zwakpEFLYmeEsFM9S8_SuK3NsoFaDZQ61f3wtCNVwUBIAniqA8CJ20Uqb79B&amp;__tn__=H-R&amp;c[0]=AT0XhQ85FG3-3DpjwxheOyqDtDPDqzDW0CeEkdc1xZyiCgywoRCMZrnPFVhOhhgPpk4rg8IgPhbqV7clzcaoHmJ5TshCqxOoK9wzglMwUPcR_jSGI3ivJQmVElNj8XEfh4XKvwtDDx3CwD736f_CFcvxB8WbkkTbcKQaSrETNYCf0LvCWgvn_vTJ
    Output: https://www.reuters.com/news/picture/thai-shelter-for-disabled-stray-dogs-thr-idUSRTX8XTG1/1550403886?fbclid=IwAR0Fd61ZalJYMVS8Cbq6KUgePJ937WGHxmRMQU59kNG4AxYzEc4fJ1t-ws8&h=AT1MPSv84XaEV7uPMPwsnZ3AGE08Iz2UYdsTAVnd7v7aMC56WgCvnMuaVMVK4CxKePDN0RD7zwakpEFLYmeEsFM9S8_SuK3NsoFaDZQ61f3wtCNVwUBIAniqA8CJ20Uqb79B&__tn__=H-R&c[0]=AT0XhQ85FG3-3DpjwxheOyqDtDPDqzDW0CeEkdc1xZyiCgywoRCMZrnPFVhOhhgPpk4rg8IgPhbqV7clzcaoHmJ5TshCqxOoK9wzglMwUPcR_jSGI3ivJQmVElNj8XEfh4XKvwtDDx3CwD736f_CFcvxB8WbkkTbcKQaSrETNYCf0LvCWgvn_vTJ

    """
    r = requests.get(fb_url)
    return r.url