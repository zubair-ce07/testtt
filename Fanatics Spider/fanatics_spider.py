import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from Spider.Fanatics.items import FanaticsItem


class FanaticsSpider(CrawlSpider):
    name = 'fanatics_spider'
    base_url = 'https://www.fanatics.com/'
    start_urls = [
        'https://www.fanatics.com/'
    ]

    menu_css = '.dropdown-link'
    product_css = '.product-image-container'

    rules = (
        Rule(LinkExtractor(restrict_css=menu_css)),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_product')
    )

    def parse_product(self, response):
        required_data = self.get_required_product_data(response)
        product = required_data['pdp-data']['pdp']
        item = FanaticsItem()
        item['product_id'] = product['productId']
        item['breadcrumb'] = self.get_product_breadcrumb(product)
        item['title'] = product['title']
        item['brand'] = product['brand']
        item['categories'] = self.get_product_categories(product)
        item['description'] = product['description']
        item['details'] = product['details']
        item['gender'] = self.get_product_gender(product)
        item['product_url'] = self.get_product_url(product)
        item['image_urls'] = self.get_product_images(product)
        item['price'] = self.get_product_price(product)
        item['currency'] = self.get_product_currency(product)
        item['language'] = self.get_product_language(response)
        item['skus'] = self.get_product_skus(product)

        yield item

    def get_required_product_data(self, response):
        required_script_xpath = '//script[contains(text(), "var __platform_data__")]/text()'
        required_script = response.xpath(required_script_xpath).extract_first()
        required_script = required_script.lstrip('var __platform_data__=')
        product_data = json.loads(required_script)
        return product_data

    def get_product_language(self, response):
        return response.xpath('/html/@lang').extract_first()

    def get_product_categories(self, product):
        return [
            category['categoryName'] for category in product['categories']
        ]

    def get_product_breadcrumb(self, product):
        return [
            breadcrumb['name'] for breadcrumb in product['breadcrumb']
        ]

    def get_product_gender(self, product):
        gender = product['genderAgeGroup']
        return gender[0] if gender else 'unisex'

    def get_product_url(self, product):
        return self.base_url + product['url']

    def get_product_price(self, product):
        price = product['price']
        discount = price['discountPrice']
        return discount['money']['value'] if discount else price['regular']['money']['value']

    def get_product_currency(self, product):
        return product['price']['regular']['money']['currency']

    def get_product_images(self, product):
        images = product['imageSelector']['additionalImages'] or [product['imageSelector']['defaultImage']]

        return [
            image['image']['src'].lstrip('//') for image in images
        ]

    def get_skus_from_sizes(self, sizes, color_name):
        skus = {}
        for size in sizes:
            if size['available']:
                skus[color_name + '_' + size['size']] = {
                    'color': color_name,
                    'size': size['size'],
                    'price': size['price']['regular']['money']['value']
                }

        return skus

    def get_product_skus(self, product):
        skus = {}
        colors = product['colors']
        if colors:
            for color in colors:
                skus.update(self.get_skus_from_sizes(color['sizes'], color['name']))

            return skus

        return self.get_skus_from_sizes(product['sizes'], 'One Color')
