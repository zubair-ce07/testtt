""" 
This module crawl pages parallely
"""
import concurrent.futures
import requests
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import urllib.request
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

URL = ['http://quotes.toscrape.com/',
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
    for data in page_data:
        quote_and_author['quote'].append(data.text.split('\n')[1])
        quote_and_author['author'].append(data.text.split('\n')[2])
    print(quote_and_author)


with ThreadPoolExecutor(max_workers=3) as executor:
    future = executor.submit(crawl_webpage, (URL[0]))
    future = executor.submit(crawl_webpage, (URL[1]))
    future = executor.submit(crawl_webpage, (URL[2]))
    future = executor.submit(crawl_webpage, (URL[3]))
    future = executor.submit(crawl_webpage, (URL[4]))