import tldextract
from bs4 import BeautifulSoup
from bias import Bias
from make_request import make_request_sleep
from url_normalize import url_normalize
from urllib.parse import urlparse
from tinydb import TinyDB
from tqdm import tqdm

# Constants
MEDIA_BIAS_SOURCE = 'https://mediabiasfactcheck.com/'
MEDIA_BIAS_CATEGORIES = ['left', 'leftcenter', 'center', 'right-center', 'right']
CATEGORY_TO_ENUM = dict(zip(MEDIA_BIAS_CATEGORIES, [e for e in Bias]))


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

        result = make_request_sleep(curr_bias_url)

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
    result = make_request_sleep(link)
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

if __name__ == "__main__":
    create_bias_db('media_bias_db.json')
    