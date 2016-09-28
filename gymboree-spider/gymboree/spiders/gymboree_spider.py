from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from gymboree.items import GarmentItem
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
        """For a given item url response, populates and yields a Garment 
        Item"""
        garment_item = GarmentItem()
        garment_item['currency'] = self.garment_currency(response)
        garment_item['price'] = self.garment_price(response)
        garment_item['description'] = self.garment_description(response)
        garment_item['retailer_sku'] = self.garment_retailer_sku(response)
        garment_item['trail'] = self.garment_url_trail(response)
        garment_item['url'] = self.garment_url(response)
        garment_item['gender'] = self.garment_gender(response)
        garment = self.garment(response)
        garment_item['image_urls'] = self.garment_image_url(garment)
        garment_item['skus'] = self.garment_skus(garment, garment_item)
        garment_item['name'] = self.garment_name(garment)
        garment_item['brand'] = self.garment_brand()
        garment_item['market'] = self.garment_market()
        garment_item['retailer'] = self.garment_retailer()
        garment_item['spider_name'] = self.spider_name()

        yield garment_item

    def spider_name(self):
        """ Returns the name of the current spider """
        return self.name

    def garment_url(self, response):
        """ Returns the url the current http response """
        return response.url

    def garment_name(self, garment):
        """ Returns the name of the current garment """
        return garment['name']

    def garment_brand(self):
        """ Returns the name of brand """
        return 'gymboree'

    def garment_currency(self, response):
        """ Returns the currency being used """
        return response.css("#pdp-price> meta::attr(content)").extract_first()

    def garment_description(self, response):
        """ Returns the description of the current garment """
        description = response.css(
            "ul[itemprop=description]> li::text").extract()
        return description[1:]

    def garment_gender(self, response):
        """ Returns the gender of the garment """
        trail_checkpoints = response.css(
            "li[itemprop=itemListElement]").extract()
        for trail_checkpoint in trail_checkpoints:
            checkpoint = trail_checkpoint.lower()
            if 'boy' in checkpoint:
                return 'Boys'
            if 'girl' in checkpoint:
                return 'Girls'
            if 'uni' in checkpoint:
                return 'Universal'

    def garment(self, response):
        """ Returns json object that has all the relevant product
        information in the webpage """
        js_element = response.xpath("//head/script[contains("
                                    "text(), 'var dataobj')]").extract_first()
        garment_found = re.search('var dataobj = (.+?);\n', js_element)
        garment_info_json = garment_found.group(1)
        return json.loads(garment_info_json)['product']

    def garment_image_url(self, garment_info):
        """ Returns the urls of all garment colors """
        return [item_color['image'] for item_color in garment_info['color']]

    def garment_market(self):
        """ Returns the market name """
        return 'US'

    def garment_price(self, response):
        """ Returns the price of the current garment """
        return response.css("span#pdp-regular-price::text").extract_first()

    def garment_retailer(self):
        """ Returns the retailer of the current garment """
        return 'gymboree'

    def garment_retailer_sku(self, response):
        """ Returns the retailer SKU of the current garment """
        return response.css("span[itemprop=mpn]::text").extract_first()

    def garment_skus(self, garment, gymboree_sale_item):
        """ Returns a list of all SKU of the current garment """
        skus = {}
        for item_color in garment['color']:
            for item_size in item_color['sizes']:
                sku = {'colour': item_color['title'],
                       'currency': gymboree_sale_item['currency'],
                       'out_of_stock': not item_size['instock'],
                       'previous_price': item_size['salePrice'],
                       'price': item_color['listPrice'],
                       'size': item_size['title']}
                skus[item_size['id']] = sku
        return skus

    def garment_url_trail(self, response):
        """ Returns the navigation trail of the current garment """
        return response.css("#pdp-breadcrumbs> li>a::attr(href)").extract()