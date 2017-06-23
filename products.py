from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractor import LinkExtractor
from ..items import ProductItem
import json
import time


class ProductSpider(CrawlSpider):
    name = "products"
    allowed_domains = ["alexachung.com"]
    start_urls = [
        'https://www.alexachung.com/uk/',
    ]

    rules = [Rule(LinkExtractor(allow=['.*\/uk\/([a-z]|-|\/|[0-9])+$']), 'parse_products', follow=True)]

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
                item_product_ids[product_key].update(price)
                item_product_ids[product_key].update({'color': 'blue'})
                item_product_ids[product_key].update({'currency': 'GBP'})
                return {'skus': item_product_ids}
        return {'skus': {}}

    def get_retailer_sku(self, response):
        product_id = response.css('.price-box.price-final_price')
        return {'retailer_sku': product_id.css('::attr(data-product-id)').extract_first()}

    def get_price(self, response):
        return {'price': response.css('.price-wrapper .price::text').extract_first()}

    def get_url(self, response):
        return {'url': response.url}

    def get_name(self, response):
        return {'name': response.css('.page-title::text').extract_first()}

    def get_description(self, response):
        description = response.css('.value')
        return {'description': description.css('p::text').extract()}

    def get_image_urls(self, response):
        images = response.css('.MagicZoom::attr(href)').extract()
        return {'image_urls': images}

    def construct_output(self, response, output):
        output['description'] = self.get_description(response)
        output['image_urls'] = self.get_image_urls(response)
        output['retailer_sku'] = self.get_image_urls(response)
        output['name'] = self.get_image_urls(response)
        output['url'] = self.get_image_urls(response)
        output['skus'] = self.get_skus(response)
        output['gender'] = 'female'
        output['brand'] = 'Alexa Chung'
        output['date'] = time.strftime("%H:%M:%S")

        return output

    def parse_products(self, response):
        yield self.construct_output(response, ProductItem())
