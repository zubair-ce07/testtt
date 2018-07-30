import requests
import json
from parsel import Selector
from Product_details import Product


class UpsideSportCrawler(object):

    def __init__(self):
        self.visited_urls = []

    def parse_category(self, url):

        selector = Selector(requests.get(url).text)
        products_urls = selector.css(
            '.product-item-link::attr(href)').extract()

        for product_url in products_urls:
            if(product_url not in self.visited_urls):
                product = Product().parse_product(product_url)
                print(json.dumps(product, indent=4))
                self.visited_urls.append(product_url)

        next_page = selector.css('.action.next::attr(href)').get()
        self.parse_category(next_page) if next_page else None

    def parse_url(self, url):

        selector = Selector(requests.get(url).text)
        categories_urls = selector.css(
            '.nav-item.level2 > a::attr(href)').extract()
        sale_men_url = selector.css(
            '.nav-item.level1.nav-5-1 > a::attr(href)').extract()
        sale_women_url = selector.css(
            '.nav-item.level1.nav-5-2 > a::attr(href)').extract()

        categories_urls.extend(sale_men_url)
        categories_urls.extend(sale_women_url)

        for url in categories_urls:
            self.parse_category(url)


def main():

    us_crawler = UpsideSportCrawler()
    us_crawler.parse_url("https://www.theupsidesport.com/")


if __name__ == '__main__':
    main()
