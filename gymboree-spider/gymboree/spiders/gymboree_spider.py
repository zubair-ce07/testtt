from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from gymboree.items import GymboreeItem, Skus
import re
import json


class GymboreeSpider(CrawlSpider):
    name = 'gymboree_spider'
    allowed_domains = ['gymboree.com']
    start_urls = ['http://www.gymboree.com/']
    rules = (
        Rule(LinkExtractor(
            restrict_css=["ul.nav-pills> li > a",
                          "li> a[foldertype=categoryLink]",
                          "a[class='next']"])),
        Rule(LinkExtractor(
            restrict_css="div.product-name> a"), callback='parse_sale_item'),
    )

    def parse_sale_item(self, response):
        gymboree_sale_item = GymboreeItem()
        gymboree_sale_item['currency'] = self.get_item_currency(
            response)
        gymboree_sale_item['price'] = self.get_item_price(response)
        gymboree_sale_item[
            'description'] = self.get_item_description(response)
        gymboree_sale_item['retailer_sku'] = self.get_item_sku(
            response)
        gymboree_sale_item['trail'] = self.get_item_url_trail(
            response)
        gymboree_sale_item['url'] = self.get_item_url(response)
        gymboree_sale_item['gender'] = self.get_item_gender(response)

        product = self.get_product(response)
        gymboree_sale_item['image_urls'] = self.get_item_image_url(
            product)
        gymboree_sale_item['skus'] = self.get_item_skus_list(
            product, gymboree_sale_item)
        gymboree_sale_item['name'] = self.get_item_name(product)
        gymboree_sale_item['brand'] = self.get_item_brand()
        gymboree_sale_item['market'] = self.get_item_market()
        gymboree_sale_item['retailer'] = self.get_item_retailer()
        gymboree_sale_item['spider_name'] = self.get_spider_name()

        yield gymboree_sale_item

    def get_spider_name(self):
        return self.name

    def get_item_url(self, response):
        return response.url

    def get_item_name(self, product):
        return product['name']

    def get_item_brand(self):
        return 'gymboree'

    def get_item_currency(self, response):
        return response.css(
            "#pdp-price> meta::attr(content)").extract_first()

    def get_item_description(self, response):
        description = response.css(
            "ul[itemprop=description]> li::text").extract()
        return description[1:]

    def get_item_gender(self, response):
        trail_checkpoints = response.css(
            "li[itemprop=itemListElement]").extract()
        for trail_checkpoint in trail_checkpoints:
            if 'boy' in trail_checkpoint.lower():
                return 'Boys'
            if 'girl' in trail_checkpoint.lower():
                return 'Girls'
            if 'uni' in trail_checkpoint.lower():
                return 'Universal'

    def get_product(self, response):
        js_element = response.xpath("//head/script[contains("
                                    "text(), 'var dataobj')]").extract_first()
        product_found = re.search('var dataobj = (.+?)};', js_element)
        product_info_json = product_found.group(1) + '}'
        return json.loads(product_info_json)['product']

    def get_item_image_url(self, product_info):
        return [item_color['image'] for item_color in product_info[
            'color']]

    def get_item_market(self):
        return 'US'

    def get_item_price(self, response):
        return response.css(
            "span#pdp-regular-price::text").extract_first()

    def get_item_retailer(self):
        return 'gymboree'

    def get_item_sku(self, response):
        return response.css("span[itemprop=mpn]::text").extract_first()

    def get_item_skus_list(self, product, gymboree_sale_item):
        skus_list = {}
        for item_color in product['color']:
            for item_size in item_color['sizes']:
                skus = Skus()
                skus['colour'] = item_color['title']
                skus['currency'] = gymboree_sale_item['currency']
                skus['out_of_stock'] = not item_size['instock']
                skus['previous_price'] = item_size['salePrice']
                skus['price'] = item_color['listPrice']
                skus['size'] = item_size['title']
                skus_list[item_size['id']] = skus
        return skus_list

    def get_item_url_trail(self, response):
        return response.css("#pdp-breadcrumbs> li>a::attr(href)").extract()
