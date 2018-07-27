import requests
from parsel import Selector
from Product_details import Product


class UpsideSportCrawler(object):

    def __init__(self):
        self.visited_urls = []
        self.products = []

    def parse_category(self, url):

        selector = Selector(requests.get(url).text)

        products_urls = selector.css(
            '.product-item-link::attr(href)').extract()

        for product_url in products_urls:

            if(product_url not in self.visited_urls):

                product = Product(product_url).parse_product()

                self.products.append(product)

                self.visited_urls.append(product_url)

        next_page = selector.css('.action.next::attr(href)').get()

        self.parse_category(next_page) if next_page else None


def parse_url(url):

    selector = Selector(requests.get(url).text)

    categories_urls = selector.css(
        '.nav-item.level2 > a::attr(href), .nav-item.level1.nav-5-1 > a::attr(href), .nav-item.level1.nav-5-2 > a::attr(href)').extract()

    return categories_urls


def print_products(upside_crawler):

    for product in upside_crawler.products:
        print(product)


def main():

    categories_urls = parse_url("https://www.theupsidesport.com/")

    us_crawler = UpsideSportCrawler()

    for url in categories_urls:
        us_crawler.parse_category(url)

    print_products(us_crawler)


if __name__ == '__main__':
    main()
