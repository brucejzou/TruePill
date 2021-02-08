import requests
import random
import time
import tldextract
from bs4 import BeautifulSoup
from bias import Bias
from url_normalize import url_normalize
from urllib.parse import urlparse
from tinydb import TinyDB
from tqdm import tqdm

# Constants
MEDIA_BIAS_SOURCE = 'https://mediabiasfactcheck.com/'
MEDIA_BIAS_CATEGORIES = ['left', 'leftcenter', 'center', 'right-center', 'right']
CATEGORY_TO_ENUM = dict(zip(MEDIA_BIAS_CATEGORIES, [e for e in Bias]))
HEADERS_LIST = [
    # Firefox 77 Mac
     {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    },
    # Firefox 77 Windows
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    },
    # Chrome 83 Mac
    {
        "Connection": "keep-alive",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://www.google.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
    },
    # Chrome 83 Windows 
    {
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://www.google.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9"
    }
]


def create_bias_db(bias_db_path):
    """
    Creates a media bias database.

    Arguments
    ----------
    bias_db_path: (string), the path to save a new database. 
    """

    db = TinyDB(bias_db_path)
    db.truncate()

    for category in MEDIA_BIAS_CATEGORIES: # Loop over political bias pages
        curr_bias_url = MEDIA_BIAS_SOURCE + category
        curr_bias = CATEGORY_TO_ENUM[category]
        print('======= PARSING ' + str(curr_bias) + ' =======')

        result = make_request(curr_bias_url)

        if result.status_code == 200:
            content = result.content
            soup = BeautifulSoup(content, features='html.parser')
            rows = soup.find_all('tr')
            random.shuffle(rows)
            for row in tqdm(rows, position=0, leave=True): # Loop over each news outlet on the bias page
                link_tag = row.find('a')
                if link_tag:
                    link = link_tag['href']
                    name, url = parse_specific_media_link(link)
                    if name and url:
                        tld = tldextract.extract(url).domain

                        # Insert current outlet's name, url, top level domain, and bias into db
                        curr_media_info = {
                            'name': name,
                            'url': url,
                            'domain_name': tld,
                            'bias': curr_bias.name
                        }

                        db.insert(curr_media_info)

def parse_specific_media_link(link):
    """
    Takes a mediabiasfactcheck link (ex: https://mediabiasfactcheck.com/geek-com/) and parses the title and source
    as the news outlet's name and link.
    
    Arguments
    ----------
    link: (string), specific news outlet link on mediabiasfactcheck.com to parse.
    """
    result = make_request(link)
    if result.status_code == 200:
        content = result.content
        soup = BeautifulSoup(content, features='html.parser')
        try:
            news_name = soup.find('h1', class_='entry-title page-title').text.strip()
            news_link = get_news_link(soup)

            if news_link and news_link[-1] != '/':
                news_link += '/'

            return news_name, news_link
        except Exception:
            print(link)
            
    return None, None

def get_news_link(soup):
    possible_indicators = ['Source', 'Sources', 'Notes']
    for indicator in possible_indicators:
        matches = soup.select('p:-soup-contains("{}:")'.format(indicator))
        for match in matches:
            if match.find('a'):
                return match.find('a')['href']
    return None
    

def make_request(url):
    """
    Helper function for making requests to randomize header and sleep time.

    Arguments
    ----------
    url: (string), url to call requests.get on.
    """
    headers = random.choice(HEADERS_LIST)
    r = requests.get(url, headers=headers)
    time.sleep(random.uniform(1,4))
    return r

if __name__ == "__main__":
    create_bias_db('media_bias_db.json')
    