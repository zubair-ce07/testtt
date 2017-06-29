from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractor import LinkExtractor
from ..items import ProductInfo
import json
import time


class AlexaChungSpider(CrawlSpider):
    name = 'alexachung'
    allowed_domains = ['alexachung.com']
    start_urls = [
        'https://www.alexachung.com/uk',
    ]

    rules = [Rule(LinkExtractor(restrict_css='.sub-menu')),
             Rule(LinkExtractor(restrict_css='.product-items'), callback='parse_products')
             ]

    def get_colour(self, response):
        _, colour, _ = response.url.rsplit('-', 2)
        return colour

    def get_skus(self, response):
        try:
            item_details = json.loads(response.css('.swatch-opt + script::text').
                                      extract_first())['[data-role=swatch-options]']\
                                                        ['Magento_Swatches/js/swatch-renderer']
        except TypeError:
            return {}

        skus = item_details['jsonConfig']['index']
        size_per_sku = item_details['jsonSwatchConfig']
        sizes_per_type = {}
        for sku_id in size_per_sku:
            for sku_type, sku_info in size_per_sku[sku_id].iteritems():
                sizes_per_type.update({sku_info['value']: {sku_id: sku_type}})
        for sku, size in zip(skus, sizes_per_type):
            skus[sku] = {'size': size, 'price': self.get_price(response),
                         'colour': self.get_colour(response), 'currency': 'GBP'}
        return {'skus': skus}

    def get_retailer_sku(self, response):
        return response.css('.price-final_price::attr(data-product-id)').extract_first()

    def get_price(self, response):
        return response.css('.price-wrapper .price::text').extract_first()

    def get_name(self, response):
        return response.css('.page-title::text').extract_first()

    def get_description(self, response):
        description = response.css('.value')
        return description.css('p::text').extract()

    def get_image_urls(self, response):
        images = response.css('.MagicZoom::attr(href)').extract()
        return images

    def parse_products(self, response):
        output = ProductInfo()
        output['description'] = self.get_description(response)
        output['image_urls'] = self.get_image_urls(response)
        output['retailer_sku'] = self.get_retailer_sku(response)
        output['skus'] = self.get_skus(response)
        output['name'] = self.get_name(response)
        output['url'] = response.url
        output['gender'] = 'female'
        output['brand'] = 'Alexa Chung'
        output['date'] = time.strftime("%H:%M:%S")
        return output
