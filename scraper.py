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


if __name__ == "__main__":
    cloth_reg = "https://www.liujo.com/gb/chino-corto-reg-w-12.html"
    cloth_dis = "https://www.liujo.com/gb/short-con-applicazioni-12.html"
    cloth_out = "https://www.liujo.com/gb/shorts-c-cintura-12.html"
    shoes_reg = "https://www.liujo.com/gb/sandalo-111.html"
    shoes_dis = "https://www.liujo.com/gb/mocassino-tc-90-tortora-7.html"
    shoes_out = "https://www.liujo.com/gb/ciabattina-tavolara-12.html"
    thing_reg = "https://www.liujo.com/gb/xs-crossbody-gioia-4.html"
    thing_dis = "https://www.liujo.com/gb/s-cross-body-arizona-2.html"
    thing_out = "https://www.liujo.com/gb/xs-crossbody-baltimora-3.html"
    onesku_reg = "https://www.liujo.com/gb/minaudiere-magenta.html"
    onesku_dis = "https://www.liujo.com/gb/xs-cross-body-maryland.html"
    kidos_mon = "https://www.liujo.com/gb/t-shirt-m-l-stripes-46.html"
    kidos_age = "https://www.liujo.com/gb/pant-lungo-jersey-fashion-10.html"
    product_L = "https://www.liujo.com/gb/calzamaglia-shoes-3.html"
    T_U_case = "https://www.liujo.com/gb/m-satchel-manhattan-11-1.html?color=5955"
    test = "https://www.liujo.com/gb/minaudiere-magenta-2.html"
    scraper = Scraper(test)
    products = scraper.scrap()
    print(len(products), products)