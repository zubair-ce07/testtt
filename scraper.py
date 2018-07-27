import requests
from parsel import Selector
from urllib.parse import urljoin, urlparse
from productschema import Product


class Scraper:
    def __init__(self, url):
        self.products = []
        self._url = f'{urlparse(url).scheme}://{urlparse(url).netloc}'
        self._pending_urls = {url}
        self._seen_urls = set()

    def _extract_urls(self, html):
        new_urls = set()
        selector = Selector(html)
        for anchor in selector.css('a::attr(href)').extract():
            url = urljoin(self._url, anchor)
            if url not in self._seen_urls and url.startswith(self._url):
                new_urls.add(url)
        return new_urls

    def _extract_product(self, response):
        selector = Selector(response.text)
        if selector.css('.catalog-product-view').extract_first():
            product = Product(response.url, selector)
            self.products.append(product)

    def scrap(self):
        while self._pending_urls:
            url = self._pending_urls.pop()
            if url not in self._seen_urls:
                self._seen_urls.add(url)
                response = requests.get(url)
                self._pending_urls |= self._extract_urls(str(response.text))
                self._extract_product(response)
        return self.products
