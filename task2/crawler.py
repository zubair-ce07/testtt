"""
this module crawl web page and get useful data.
"""
import requests
from bs4 import BeautifulSoup


class CrawlQuotes:
    """The class hold quotes and authors """
    def __init__(self):
        self.quote = []
        self.author = []

    def crawl_webpage(self):
        """The method get page data and populate useful data"""
        url = 'http://quotes.toscrape.com/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        required_data = soup.find_all('span')

        for index in range(0, 20, 2):
            self.quote.append(required_data[index].text)
            self.author.append(required_data[index+1].text.split('\n')[0])
        print(self.quote)
        print()
        print(self.author)

if __name__ == "__main__":
    crawling = CrawlQuotes()
    crawling.crawl_webpage()
