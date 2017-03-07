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

        Rule(LinkExtractor(allow=('/collections/.*/products/',),
                           restrict_css=("div.product-card.-content-overlay",)),
             callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=('/collections/',)), follow=True),
    )

    def parse_item(self, response):
        product = KithItem()

        product['url'] = response.url
        product['brand'] = self.product_brand(response)
        product['category'] = self.product_category(response)

        self.product_description_and_care(response, product)

        product['image_urls'] = self.image_urls(response)
        product['industry'] = ''
        product['market'] = 'US'
        product['merch_info'] = []

        sku_content = re.split(r"variants\":", self.get_sku_content(response))
        product['retailer_sku'] = self.retailer_sku(response)
        product['skus'] = self.skus(sku_content[1], response)
        product['gender'] = self.gender(sku_content[0])

        product['name'] = product['category'][0]
        product['retailer'] = 'kith-us'

        return product

    def get_sku_content(self, response):
        pattern = re.compile(r"product:(.*?),\"imag", re.MULTILINE | re.DOTALL)
        return response.xpath("//script[contains(.,'product:')]/text()").re(pattern)[0]

    def product_brand(self, response):
        return response.css('h1.product-header-title span::text').extract()

    def product_category(self, response):
        return response.css('.breadcrumb.text-center a[href^="/c"]::text').extract()

    def product_description_and_care(self, response, product):
        parent_class = response.css('.product-single-details-rte')
        product['description'] = parent_class.css('p::text').extract()[:-2]
        product['care'] = parent_class.css('p:last-child::text').extract()

    def image_urls(self, response):
        image_urls = response.xpath("//meta[@property='og:image:secure_url']"
                                    "/@content").extract()
        return [url.replace('_grande', "") for url in image_urls]

    def gender(self, script):
        if "wmns" in script:
            return "women"
        else:
            return "men"

    def retailer_sku(self, response):
        return response.css('input#product_id::attr(value)').extract_first()

    def skus(self, script, response):
        variants = json.loads(script)

        skus = {}

        for variant in variants:
            sku = {}
            sku['price'] = variant['price']
            sku['currency'] = 'USD'
            sku['out_of_stock'] = variant['available']

            if variant['compare_at_price']:
                sku['previous_prices'] = [variant['compare_at_price']]

            sku['size'] = variant['title']
            sku['colour'] = response.css('.product-single-header-upper .product-'
                                         'header-title.-variant::text').extract_first().strip()
            skus[variant['id']] = sku

        return skus
