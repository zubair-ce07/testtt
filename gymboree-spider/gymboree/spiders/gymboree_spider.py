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
        garment_item['brand'] = 'gymboree'
        garment_item['market'] = 'US'
        garment_item['retailer'] = 'gymboree'
        garment_item['url'] = response.url
        garment_item['spider_name'] = self.name
        garment_item['currency'] = self.garment_currency(response)
        garment_item['price'] = self.garment_price(response)
        garment_item['care'], garment_item['description'] = \
            self.garment_description(response)
        garment_item['retailer_sku'] = self.garment_retailer_sku(response)
        garment_item['trail'] = self.garment_url_trail(response)
        garment_item['gender'] = self.garment_gender(response)
        garment_meta = self.garment_meta(response)
        garment_item['image_urls'] = self.garment_image_urls(garment_meta)
        garment_item['name'] = self.garment_name(garment_meta)
        garment_item['skus'] = self.garment_skus(garment_meta,
                                                 garment_item['currency'])
        yield garment_item

    def garment_care(self, response):
        return response.css('#pdp-product-details-more>li::text').extract()

    def garment_name(self, garment):
        """ Returns the name of the current garment """
        return garment['name']

    def garment_currency(self, response):
        """ Returns the currency being used """
        return response.css("#pdp-price> meta::attr(content)").extract_first()

    def garment_description(self, response):
        """ Returns the description of the current garment """
        care_filters = ['spot clean', 'machine wash']
        care_instructions = []
        description = response.css("ul[itemprop=description] li::text").extract()
        for index, description_line in enumerate(description):
            for care_filter in care_filters:
                if care_filter in description_line.lower():
                    care_instructions.append(description_line)
                    del description[index]
                    continue
        return (care_instructions,description)

    def garment_gender(self, response):
        """ Returns the gender of the intended garment user """
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

    def garment_meta(self, response):
        """ Returns json object that has all the relevant product
        information in the webpage """
        js_element = response.xpath("//head/script[contains("
                                    "text(), 'var dataobj')]").extract_first()
        garment_search_result = re.search('var dataobj = (.+?);\n', js_element)
        garment_info_json = garment_search_result.group(1)
        return json.loads(garment_info_json)['product']

    def garment_image_urls(self, garment_info):
        """ Returns the urls of all garment colors """
        return [color_variant['image'] for color_variant in garment_info['color']]

    def garment_price(self, response):
        """ Returns the price of the current garment """
        sale_price = response.css("#pdp-sale-price> "
                                  "span::text").extract_first()
        regular_price = response.css(
            "span#pdp-regular-price::text").extract_first()
        return sale_price or regular_price

    def garment_retailer_sku(self, response):
        """ Returns the retailer SKU of the current garment """
        return response.css("span[itemprop=mpn]::text").extract_first()

    def garment_skus(self, garment, currency):
        """ Returns a list of all SKU of the current garment """
        skus = {}
        for color_variant in garment['color']:
            for size_variant in color_variant['sizes']:
                sku = {'colour': color_variant['title'],
                       'currency': currency,
                       'out_of_stock': not size_variant['instock'],
                       'previous_price': color_variant['listPrice'],
                       'price': size_variant['salePrice'],
                       'size': size_variant['title']}
                skus[size_variant['id']] = sku
        return skus

    def garment_url_trail(self, response):
        """ Returns the navigation trail of the current garment """
        return response.css("#pdp-breadcrumbs> li>a::attr(href)").extract()
