from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractor import LinkExtractor
from ..items import ProductInfo
import json
import time


class AlexaChungSpider(CrawlSpider):
    name = 'alexachung'
    allowed_domains = ['alexachung.com']
    start_urls = [
        'https://www.alexachung.com/uk/',
    ]

    rules = [Rule(LinkExtractor(restrict_css='.sub-menu')),
             Rule(LinkExtractor(allow=['.*[a-z]+$'], restrict_css='.products.wrapper.grid.products-grid')),
             Rule(LinkExtractor(allow=['.*\/uk\/[a-z-0-9]+$']), callback='parse_products')
             ]

    def get_colour(self, response):
        _, colour, _ = self.get_url(response).rsplit('-', 2)
        return colour

    def get_skus(self, response):
        item_details = {}
        try:
            _, item_details, _ = response.css('.fieldset script::text').extract()
        except ValueError:
            pass
        if item_details:
            item_details = json.loads(item_details)['[data-role=swatch-options]']['Magento_Swatches/js/swatch-renderer']
            item_product_ids = item_details['jsonConfig']['index']
            product_labels = item_details['jsonSwatchConfig']
            price = self.get_price(response)
            for product_key, product_details in item_product_ids.iteritems():
                item_product_ids[product_key].update({'size':
                                                        product_labels[next(iter(product_labels.keys()))][next(iter(
                                                        product_details.values()))]['value']})
                item_product_ids[product_key].update({'price': price})
                item_product_ids[product_key].update({'colour': self.get_colour(response)})
                item_product_ids[product_key].update({'currency': 'GBP'})
                return item_product_ids
        return {}

    def get_retailer_sku(self, response):
        product_id = response.css('.price-box.price-final_price')
        return product_id.css('::attr(data-product-id)').extract_first()

    def get_price(self, response):
        return response.css('.price-wrapper .price::text').extract_first()

    def get_url(self, response):
        return response.url

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
        output['name'] = self.get_name(response)
        output['url'] = self.get_url(response)
        output['skus'] = self.get_skus(response)
        output['gender'] = 'female'
        output['brand'] = 'Alexa Chung'
        output['date'] = time.strftime("%H:%M:%S")
        return output
