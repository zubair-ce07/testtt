import requests
import json

from parsel import Selector
from urllib.parse import urljoin
from asics_parser import ProductParser


class AsicsSpider:

    def __init__(self, start_url):
        self.start_url = start_url
        self.allowed_domains = "www.asics.com"

    def get_page_content(self, url):
        response = requests.get(url)
        return response.text

    def extract_categories(self):
        sel = Selector(text=self.get_page_content(self.start_url))
        relative_category_urls = sel.css(".nav-item:not(.mobile) ::attr(href)").getall()
        absolute_category_urls = [urljoin(self.start_url, url) for url in relative_category_urls]
        return set([url for url in absolute_category_urls if self.allowed_domains in url])

    def parse_product_urls(self, category_urls):
        product_urls = []
        for base_url in category_urls:
            product_urls += [urljoin(base_url, url) for url in self.parse_category_page(base_url)]
        return set(product_urls)

    def goto_next_page(self, sel):
        return sel.css("#nextPageLink > a::attr(href)").get()

    def parse_category_page(self, category_url):
        relative_urls = []
        sel = Selector(text=self.get_page_content(category_url))
        next_page = self.goto_next_page(sel)
        if next_page:
            relative_urls += self.parse_category_page(urljoin(category_url, next_page))

        relative_urls += sel.css('.productMainLink::attr(href)').getall()
        return list(filter(lambda url: "//" not in url, relative_urls))

    def crawl(self):
        category_urls = self.extract_categories()
        product_urls = self.parse_product_urls(category_urls)
        products = [ProductParser(url, self.get_page_content(url)).get_product() for url in product_urls]
        print(json.dumps(products, indent=4))


def main():
    asics_crawler = AsicsSpider("http://www.asics.com/nz/en-nz/")
    asics_crawler.crawl()


if __name__ == '__main__':
    main()
