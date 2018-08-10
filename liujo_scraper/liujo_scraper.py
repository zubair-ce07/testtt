import requests
from parsel import Selector
from liujo_scraper.product_schema import parse_product


class Scraper:
    def __init__(self, url):
        self.products = []
        self._url = url
        self._pending_urls = {url}
        self._seen_urls = set()

    def _extract_urls(self, html):
        new_urls = set()
        selector = Selector(html)
        for url in selector.css('a::attr(href)').extract():
            if url not in self._seen_urls and url.startswith(self._url):
                new_urls.add(url)
        return new_urls

    def _extract_product(self, response):
        selector = Selector(response.text)
        if selector.css('.catalog-product-view').extract_first():
            print(response.url)
            product = parse_product(response)
            print(product)
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


if __name__ == "__main__":
    scraper = Scraper('https://www.liujo.com/gb/')
    products = scraper.scrap()
    print(len(products), products)
