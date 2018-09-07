"""
this module make thread and crawl page concurrently
"""
import threading
import requests
from bs4 import BeautifulSoup

URL = 'http://quotes.toscrape.com/'
quote_and_author = {'quote': [], 'author': []}


def get_page(url):
    """This method get url from thread and crawl page"""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    page_data = soup.find_all(
        lambda tag: tag.name == 'div' and tag['class'] == ['quote'])
    for data in page_data:
        quote_and_author['quote'].append(data.text.split('\n')[1])
        quote_and_author['author'].append(data.text.split('\n')[2])
    print()
    print(quote_and_author)
    next_page_url = get_url(soup)
    if next_page_url:
        get_page(next_page_url)


def get_url(soup):
    """This method get next page url"""
    next_page = soup.find(lambda tag: tag.name ==
                          'li' and tag['class'] == ['next'])
    html_text = str(next_page)
    start_page = html_text.find('/page')
    link = html_text[start_page+1:35]
    if link == 'None':
        return 0
    else:
        next_page_url = URL + link
        return next_page_url


page_thread = threading.Thread(target=get_page(URL))
print(' thread started')
page_thread.start()
