from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import time
import re
import os


class PyDocsSpider:

    MAX_DEPTH = 2
    OUTPUT_PATH = 'Output/'
    DOWNLOAD_DELAY = 2
    START_URL = 'https://docs.python.org/3/index.html'
    ALLOWED_URL_REGEX = re.compile(r'^https://docs\.python\.org/3/.+$')

    def __init__(self):
        self.visited_links = set()

    def download_page(self, url):
        print("Requesting URL: "+ url)
        time.sleep(self.DOWNLOAD_DELAY)
        response = requests.get(url)
        self.save_page(url, response.text)
        self.visited_links.add(url)
        return response.text

    def is_visited(self, url):
        if url in self.visited_links:
            return True
        return False

    def is_page_allowed(self, url):
        if self.ALLOWED_URL_REGEX.match(url):
            return True
        return False

    def url_to_dirpath(self, url):
        return url.replace('https://docs.python.org/3/', self.OUTPUT_PATH)

    def save_page(self, url, page_content):
        filepath = self.url_to_dirpath(url)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as page:
            page.write(page_content)

    def canonical_url(self, base_url, url):
        if '#' in url:
            url = url.split('#')[0]
        return urljoin(base_url, url)

    def start_crawling(self):
        self.crawl_url(self.START_URL)

    def crawl_url(self, base_url, depth=0):
        if depth == self.MAX_DEPTH:
            return

        page_source = self.download_page(base_url)
        soup = BeautifulSoup(page_source, 'lxml')

        for link in soup('a'):
            url = self.canonical_url(base_url, link.get('href'))
            if self.is_page_allowed(url) and not self.is_visited(url):
                self.crawl_url(url, depth + 1)


if __name__ == '__main__':

    py_docs_spider = PyDocsSpider()
    py_docs_spider.start_crawling()
