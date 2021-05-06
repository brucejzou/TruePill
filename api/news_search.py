import tldextract
from pygooglenews import GoogleNews
from datetime import timedelta
from tinydb import Query

DATE_FORMAT = "%Y-%m-%d"

def google_news_search(article_url, keywords, date, num_suggestions, sources, date_margin, bias_db):
    """
    Searches google news for `num_suggestions` articles about `keywords` around `date` from the `sources`.

    Arguments
    ----------
    article_url: (string), original article url.
    keywords: ([string]), list of keywords to search for.
    date: (datetime), date to search around. (Can be none, if so don't pass a date to search)
    num_suggestions: (int), number of articles to find.
    sources: ([string]), list of news sources to find articles from.
    bias_db: (TinyDB), media bias db.
    """

    # build query: keywords + inurl:source1 OR inurl:source2 OR etc...
    # ex: https://news.google.com/rss/search?q=Boeing+inurl:cnn OR inurl:nytimes OR inurl:washingtonpost OR inurl:foxnews&ceid=US:en&hl=en-US&gl=US
    # date, from_, to_, +- 1 week? configurable
    gn = GoogleNews()

    query_str = create_query_str(keywords, sources)
    start_date, end_date = None, None
    if date:
        start_date, end_date = get_date_range(date, date_margin)

    search = gn.search(query_str, from_=start_date, to_=end_date)
    
    # Go through search results to get article urls to return
    entries = search['entries']
    results = []
    already_chosen = set()
    already_chosen.add(tldextract.extract(article_url).domain) # add original article domain to no pick from there again.
    if sources:
        for entry in entries:
            entry_domain_name = tldextract.extract(entry.source['href']).domain
            if entry_domain_name in sources and entry_domain_name not in already_chosen:
                already_chosen.add(entry_domain_name)
                results.append((entry.title, entry.link))

    else: # if no sources given, just get first num_suggestion articles that have source in bias_db
        Media = Query()
        for entry in entries:
            entry_domain_name = tldextract.extract(entry.source['href']).domain
            if bias_db.search(Media.domain_name == entry_domain_name) and entry_domain_name not in already_chosen:
                already_chosen.add(entry_domain_name)
                results.append((entry.title, entry.link))
            if len(results) == num_suggestions:
                break

    return results

def create_query_str(keywords, sources):
    """
    Creates the query string to search for `keywords` from `sources`.

    Arguments
    ----------
    keywords: ([string]), list of keywords to search for.
    sources: ([string]), list of news sources to find articles from.
    """
    str_builder = keywords.copy()
    for source in sources:
        str_builder.append('inurl:' + source)
        str_builder.append('OR')
    if len(str_builder) > 0  and str_builder[-1] == 'OR':
        del str_builder[-1]
    
    return ' '.join(str_builder)

def get_date_range(date, margin):
    """
    Returns the start and end date range for date-margin to date+margin as strings in DATE_FORMAT.

    Arguments
    ----------
    date: (datetime), a date time.
    margin: (int), margin of time (in days) to add and subtract from date.
    """
    time_delta = timedelta(days=margin)
    start_date = date - time_delta
    end_date = date + time_delta
    return start_date.strftime(DATE_FORMAT), end_date.strftime(DATE_FORMAT)
