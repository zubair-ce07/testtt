import json

import requests
import parsel
from liujo_product_parse import ProductParser


def main():
    url = 'https://www.liujo.com/de'
    liujo_crawler = Crawler(url)
    liujo_crawler.crawl()


class Crawler:

    def __init__(self, url):
        self.url = url
        product_css = ".category-products a[href^='http']:not([href*='wishlist']):not([href*='p='])::attr('href')"
        self.listing_le = LinkExtractor(css="a[target='_self'][href^='http']::attr('href')")
        self.product_le = LinkExtractor(css=product_css)
        self.pagination_le = LinkExtractor(css=".pages a.next::attr(href)")
        self.product_parser = ProductParser()

    def crawl(self):
        seen_urls = set()
        listings = {self.url}
        while listings:
            url = listings.pop()
            if url in seen_urls:
                continue
            seen_urls.add(url)
            response = requests.get(url)
            listings |= set(self.listing_le.extract_links(response))
            listings |= set(self.pagination_le.extract_links(response))
            for url in set(self.product_le.extract_links(response)):
                if url in seen_urls:
                    continue
                seen_urls.add(url)
                self.parse_product(url)

    def parse_product(self, url):
        response = requests.get(url)
        print(url)
        product = self.product_parser.parse(response)
        if product:
            self.dump_product(product)

    def dump_product(self, details):
        with open(f"prod_data/{details.get('retailer_sku')}.json", 'w') as json_file:
            json.dump(details, json_file, indent=1)


class LinkExtractor:

    def __init__(self, css):
        self.css = css

    def extract_links(self, response):
        return parsel.Selector(text=response.text).css(self.css).getall()


if __name__ == '__main__':
    main()
