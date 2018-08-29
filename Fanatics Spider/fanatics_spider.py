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
        required_script_xpath = '//script[contains(text(), "var __platform_data__")]/text()'
        required_script = response.xpath(required_script_xpath).extract_first()
        required_script = required_script.lstrip('var __platform_data__=')
        required_data = json.loads(required_script)

        product = self.get_product(required_data)
        item = FanaticsItem()
        item['id'] = self.get_product_id(product)
        item['breadcrumb'] = self.get_product_breadcrumb(product)
        item['title'] = self.get_product_title(product)
        item['brand'] = self.get_product_brand(product)
        item['categories'] = self.get_product_categories(product)
        item['description'] = self.get_product_description(product)
        item['details'] = self.get_product_details(product)
        item['gender'] = self.get_product_gender(product)
        item['url'] = self.get_product_url(product)
        item['images'] = self.get_product_images(product)
        item['price'] = self.get_product_price(product)
        item['currency'] = self.get_product_currency(product)
        item['language'] = self.get_product_language(response)
        item['skus'] = self.get_product_skus(product)

        yield item

    def get_product_id(self, product):
        return product['productId']

    def get_product_language(self, response):
        lang = response.xpath('/html/@lang').extract()
        return lang

    def get_product(self, json_data):
        return json_data['pdp-data']['pdp']

    def get_product_title(self, product):
        return product['title']

    def get_product_brand(self, product):
        return product['brand']

    def get_product_categories(self, product):
        return [
            category['categoryName'] for category in product['categories']
        ]

    def get_product_breadcrumb(self, product):
        return [
            breadcrumb['name'] for breadcrumb in product['breadcrumb']
        ]

    def get_product_description(self, product):
        return product['description']

    def get_product_details(self, product):
        return product['details']

    def get_product_gender(self, product):
        gender = product['genderAgeGroup']
        return gender[0] if gender else 'unisex'

    def get_product_url(self, product):
        return self.base_url + product['url']

    def get_product_price(self, product):
        price = product['price']
        discount = price['discountPrice']
        if discount:
            return discount['money']['value']

        return price['regular']['money']['value']

    def get_product_currency(self, product):
        return product['price']['regular']['money']['currency']

    def get_product_images(self, product):
        images = product['imageSelector']['additionalImages']

        return [
            'https:' + image['image']['src'] for image in images
        ]

    def get_skus_from_sizes(self, sizes, color_name):
        for size in sizes:
            if size['available']:
                yield color_name + '_' + size['size'], {
                    'color': color_name,
                    'size': size['size'],
                    'price': size['price']['regular']['money']['value']
                }

    def get_product_skus(self, product):
        skus = {}
        colors = product['colors']
        if colors:
            for color in colors:
                skus.update({
                    key: value for key, value in self.get_skus_from_sizes(color['sizes'], color['name'])
                })
        else:
            skus = {
                key: value for key, value in self.get_skus_from_sizes(product['sizes'], 'One Color')
            }

        return skus
