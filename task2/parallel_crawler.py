"""
This module crawl pages parallely
"""
import concurrent.futures
import urllib.request
import requests
from bs4 import BeautifulSoup

URLS = ['http://quotes.toscrape.com/',
        'http://quotes.toscrape.com/page/2/',
        'http://quotes.toscrape.com/page/3/',
        'http://quotes.toscrape.com/page/4/',
        'http://quotes.toscrape.com/page/5/']
quote_and_author = {'quote': [], 'author': []}


def crawl_webpage(url):
    """The method get page data and populate useful data"""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    page_data = soup.find_all(
        lambda tag: tag.name == 'div' and tag['class'] == ['quote'])
    for data, data in enumerate(page_data):
        quote_and_author['quote'].append(data.text.split('\n')[1])
        quote_and_author['author'].append(data.text.split('\n')[2])


def load_url(url, timeout):
    """Method retrieves single page and report the url and content"""
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return conn.read()


with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    future_to_url = {executor.submit(load_url, url, 60): url for url in URLS}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
            crawl_webpage(url)
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
        else:
            print('%r page is %d bytes' % (url, len(data)))
            print(quote_and_author)
