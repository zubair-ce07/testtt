from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from kith.items import KithItem
import json
import re


class KithSpider(CrawlSpider):
    name = 'kith'
    allowed_domains = ['kith.com']
    start_urls = ['https://kith.com/']

    rules = (
        Rule(LinkExtractor(allow=('/collections/.*/products/',)),
             callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=('/collections/',)), follow=True),
    )

    def parse_item(self, response):
        product = KithItem()

        product['url'] = response.url
        product['brand'] = self.get_product_brand(response)
        product['category'] = self.get_product_category(response)

        self.get_product_details(response, product)

        product['image_urls'] = self.get_image_urls(response)
        product['industry'] = ''
        product['market'] = 'US'
        product['merch_info'] = []

        sku_content = self.get_sku_content(response).split('variants', 1)
        product['retailer_sku'] = self.get_retailer_sku(sku_content[0])
        product['skus'] = self.get_skus(sku_content[1], response)
        product['gender'] = self.get_gender(sku_content[0])

        product['name'] = product['category']
        product['retailer'] = 'kith-us'

        return product

    def get_sku_content(self, response):
        pattern = re.compile(r"product:(.*?)}]", re.MULTILINE | re.DOTALL)
        return response.xpath("//script[contains(.,'product:')]/text()").re(pattern)[0]

    def get_product_brand(self, response):
        return response.css('h1.product-header-title span::text').extract()

    def get_product_category(self, response):
        return response.css('.breadcrumb.text-center a[href^="/c"]::text').extract()

    def get_product_details(self, response, product):
        parent_class = response.css('.product-single-details-rte')
        product['description'] = parent_class.css('p::text').extract()[:-2]
        product['care'] = parent_class.css('p:last-child::text').extract()

    def get_image_urls(self, response):
        return response.css('img.full-width::attr(src)').extract()

    def get_gender(self, script):
        if "wmns" in script:
            return "women"
        else:
            return "men"

    def get_retailer_sku(self, response):
        return re.findall(r"\"id\":(.*?),", response)[0]

    def get_skus(self, script, response):
        sku_fields = json.loads((script + '}]')[2:])

        skus = {}

        for field in sku_fields:
            sku = {}
            sku['price'] = field['price']
            sku['currency'] = 'USD'
            sku['out_of_stock'] = field['available']
            sku['previous_prices'] = [field['compare_at_price']]
            sku['size'] = field['title']
            sku['color'] = response.css('.product-single-header-upper .product-'
                                        'header-title.-variant::text').extract_first().strip()
            skus[field['id']] = sku

        return skus
