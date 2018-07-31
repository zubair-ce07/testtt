import requests
import json

from parsel import Selector
from urllib.parse import urljoin, urlparse
from asics_parser import ProductParser


class AsicsSpider:

    def __init__(self, start_url):
        self.start_url = start_url
        self.network_location = urlparse(start_url).netloc

    def get_page_content(self, url):
        with requests.get(url) as response:
            return response.text

    def extract_categories(self):
        sel = Selector(text=self.get_page_content(self.start_url))
        relative_category_urls = sel.css(".nav-item:not(.mobile) ::attr(href)").getall()
        absolute_category_urls = [urljoin(self.start_url, url) for url in relative_category_urls]
        return set([url for url in absolute_category_urls if self.network_location in url])

    def extract_product_urls(self, category_urls):
        return set(sum([self.get_absolute_urls(url) for url in category_urls], []))

    def get_absolute_urls(self, category_url):
        page_no = 0
        relative_urls = []
        sel = Selector(text=self.get_page_content(category_url))
        product_page_class = sel.css("body::attr(class)").get()
        page_not_found_class = ["server-error-body", "page-notFound"]

        while not any(error_page in product_page_class for error_page in page_not_found_class):  # If page exists
            page_no += 1
            relative_urls += sel.css('.productMainLink::attr(href)').getall()
            sel = Selector(text=self.get_page_content(f'{category_url}?page={page_no}'))         # Move to next page
            product_page_class = sel.css("body::attr(class)").get()

        filtered_urls = filter(lambda url: "//" not in url, set(relative_urls))                  # Remove invalid urls
        return [urljoin(self.start_url, url) for url in filtered_urls]

    def get_json_result(self, products):
        print(json.dumps(products, indent=4))

    def crawl(self):
        category_urls = self.extract_categories()
        product_urls = self.extract_product_urls(category_urls)
        products = [ProductParser(url, self.get_page_content(url)).get_product() for url in product_urls]
        self.get_json_result(products)


def main():
    asics_crawler = AsicsSpider("http://www.asics.com/nz/en-nz/")
    asics_crawler.crawl()


if __name__ == '__main__':
    main()
