import json
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class WoolworthSpider(CrawlSpider):
    name = 'woolworths'
    allowed_domains = ['woolworths.co.za']
    start_urls = ['https://woolworths.co.za']
    download_delay = 3

    rules = (
        Rule(LinkExtractor(restrict_css=['.main-nav__list-item--secondary .main-nav__link',
                                         '.pagination'])),
        Rule(LinkExtractor(restrict_css='.product-card__visual'), callback='parse_products')
    )

    def parse_products(self, response):
        resp = response.css('body > script::text').extract_first()
        json_resp = json.loads(resp.split('= ')[1])
        item = {
            'description': self.extract_description(response),
            'type': self.extract_product_type(json_resp),
            'image_urls': self.extract_image_urls(json_resp),
            'product_name': self.extract_product_name(json_resp),
            'sku': self.extract_sku_id(json_resp),
            'url': response.url,
            'skus': self.extract_product_skus(json_resp)
        }
        yield item

    def extract_product_skus(self, json_resp):
        items = {
            'skus': {}
        }
        price = self.extract_price(json_resp)
        for col in self.extract_colors(json_resp):
            for size in self.extract_sizes(json_resp):
                values = {
                    'color': col,
                    'price': price,
                    'size': size
                }
                items['skus']['{0}_{1}'.format(size, col)] = values
            return items['skus']

    def extract_product_type(self, response):
        prod_type = response['pdp']['productInfo']['breadcrumbs']['default']
        return [items[key] for items in prod_type for key in items if key == 'label']

    def extract_colors(self, response):
        color = response['pdp']['productInfo']['colourSKUs']
        return [items[key] for items in color for key in items if key == 'colour']

    def extract_price(self, json_resp):
        return json_resp['pdp']['productPrices'][self.extract_sku_id(json_resp)]['plist3620008']['priceMax']

    def extract_sizes(self, response):
        items = response['pdp']['productInfo']['styleIdSizeSKUsMap'].values()[0]
        return [size[key] for size in items for key in size if key == 'size']

    def extract_image_urls(self, response):
        items = response['pdp']['productInfo']['colourSKUs']
        image_url = [url[key] for url in items for key in url if key == 'externalImageUrlReference']
        return ['https://woolworths.co.za/{0}'.format(image) for image in image_url]

    def extract_description(self, response):
        return ''.join(self.clean_spaces(desc) for desc in response.css('.accordion--chrome .accordion__segment--chrome > '
                                                              ' div ::text').extract()[:-2])

    def extract_sku_id(self, response):
        return response['pdp']['productInfo']['productId']

    def extract_product_name(self, response):
        return response['pdp']['productInfo']['displayName']

    def clean_spaces(self, str):
        return ' '.join(re.split("\s+", str, flags=re.UNICODE))
