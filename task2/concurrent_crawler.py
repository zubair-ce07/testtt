"""
this module make thread and crawl page concurrently
"""
import threading
import requests
from bs4 import BeautifulSoup

URLS = ['http://quotes.toscrape.com/',
        'http://quotes.toscrape.com/page/2/']
quote_and_author = {'quote': [], 'author': []}


def get_page(url):
    """This method get url from thread and crawl page"""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    page_data = soup.find_all(
        lambda tag: tag.name == 'div' and tag['class'] == ['quote'])
    for data, data in enumerate(page_data):
        quote_and_author['quote'].append(data.text.split('\n')[1])
        quote_and_author['author'].append(data.text.split('\n')[2])


page_thread = threading.Thread(target=get_page(URLS[0]))
print(' first thread started')
print()
print(quote_and_author)
page_thread.start()
page_thread = threading.Thread(target=get_page(URLS[1]))
page_thread.start()
print(' Second thread started')
print()
print(quote_and_author)
