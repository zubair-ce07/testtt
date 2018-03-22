"""
Spider to crawl all products in ernstings-family.de website
Example command from terminal: $ scrapy crawl ernstings -o ernstings.json
Pylint score: 10.00
"""

import re
import scrapy                           # pylint: disable=import-error


class ErnstingsSpider(scrapy.Spider):
    """Spider to crawl all products in ernstings-family.de website"""
    name = "ernstings"
    start_urls = ['https://www.ernstings-family.de']
    allowed_domains = ['ernstings-family.de']

    def __init__(self):
        self.store_urls = []
        self.products_urls = []
        self.products = []

    def parse(self, response):
        """Parsing homepage and getting urls for category pages"""
        for each in response.css('a.nav-link::attr(href)'):
            if each not in self.store_urls:
                self.store_urls.append(each.extract())
        for each in response.css('a.link-blank::attr(href)'):
            if each not in self.store_urls:
                self.store_urls.append(each.extract())

        for page in self.store_urls:
            yield response.follow(page, callback=self.parse_store)

    def parse_store(self, response):
        """Parsing category pages and getting urls for products pages"""
        for each in response.css('a.nav-link::attr(href)'):
            if each not in self.store_urls:
                self.store_urls.append(each)
        for each in response.css('a.link-blank::attr(href)'):
            if each not in self.store_urls:
                self.store_urls.append(each.extract())

        for each in response.css('a.product-list-tile-holder.link-blank::attr(href)'):
            if each not in self.products_urls:
                self.products_urls.append(each.extract())

        for page in self.products_urls:
            yield response.follow(page, callback=self.parse_product)

    def parse_product(self, response):      # pylint: disable=too-many-locals
        """Parsing product and getting required details"""
        url = response.url
        name = response.css('h1.product-detail-product-name::text').extract_first()
        label = response.css('span.label-text::text').extract()
        images = response.css('img.product-view-slide-image::attr(src)').extract()
        description = response.css('header.product-detail-headline + p::text').extract_first()
        price = response.css('span.product-price::text').extract()
        sizes = response.css('select#select-size-product-detail :not(option:disabled)::text')
        color = response.css('p.product-detail-product-color::text').extract_first()

        name = remove_formatting(name)
        description = remove_formatting(description)
        color = remove_formatting(color)

        if len(price) == 2:
            actual = remove_formatting(price[0])
            discounted = remove_formatting(price[1])
        else:
            actual = remove_formatting(price[0])
            discounted = remove_formatting(price[0])

        store = []
        if not sizes or sizes.extract() == ['-']:
            sku = {
                'sku_id': name,
                'price': discounted,
                'size': None,
                'color': color
            }
            store.append(sku)
        else:
            for size in sizes.extract():
                sku = {
                    'sku_id': name + '_' + size,
                    'price': discounted,
                    'size': size,
                    'color': color
                }
                store.append(sku)

        product = {
            'url': url,
            'name': name,
            'label': label,
            'image_urls': ['https:{}'.format(image) for image in images],
            'description': description,
            'actual_price': actual,
            'discount_price': discounted,
            'sku': store
        }
        self.products.append(product)
        yield product


def remove_formatting(text):
    """Function to remove \n \t etc"""
    return re.sub(r'\s+', ' ', text).strip()
