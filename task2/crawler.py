"""
this module crawl web page and get useful data.
"""
import requests
from bs4 import BeautifulSoup

def crawl_webpage():
    """The method get page data and populate useful data"""
    url = 'http://quotes.toscrape.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    page_data = soup.find_all(
        lambda tag: tag.name == 'div' and tag['class'] == ['quote'])
    quote_and_author = {'quote': [], 'author': []}
    for data in page_data:
        quote_and_author['quote'].append(data.text.split('\n')[1])
        quote_and_author['author'].append(data.text.split('\n')[2])
    for index in range(len(quote_and_author['quote'])):
        print('Quote: ', quote_and_author['quote'][index])
        print('Author: ', quote_and_author['author'][index])
        print()


if __name__ == "__main__":
    crawl_webpage()
