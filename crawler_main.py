import requests
import json
from parsel import Selector
from Product_details import ProductParser


class UpsideSportCrawler(object):

    def __init__(self):
        self.visited_products = []

    def parse_next_page(selector):
        next_page = selector.css('.action.next::attr(href)').get()
        self.parse_category(next_page) if next_page else None

    def parse_category(self, product_id):
        if(product_id not in self.visited_products):
            product = ProductParser.parse_product(product_url)
            print(json.dumps(product, indent=4))
            self.visited_products.append(product_id)

    def parse_product_url(products_urls):
        for product_url in products_urls:
            product_id = product_url.split("/")[:-1]
            self.parse_category(product_id)

    def parse_categories(self, url):
        selector = Selector(requests.get(url).text)
        products_urls = selector.css('.product-item-link::attr(href)').extract()
        self.parse_product_url(products_urls)
        self.parse_next_page(selector)

    def filter_urls(self, categories_urls):
        return [url for url in categories_urls if url.startswith('https://')]

    def parse_url(self, url):
        selector = Selector(requests.get(url).text)
        categories_urls = selector.css('#mainmenu a::attr(href)').extract()
        valid_urls = self.filter_urls(categories_urls)

        for url in valid_urls:
            self.parse_categories(url)


def main():

    us_crawler = UpsideSportCrawler()
    us_crawler.parse_url("https://www.theupsidesport.com/")


if __name__ == '__main__':
    main()
