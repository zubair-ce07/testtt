import json
import re
from w3lib.url import add_or_replace_parameter

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = 'eloquii-us'
    market = 'US'

    start_urls = ['https://www.eloquii.com/']
    allowed_domains = ['eloquii.com']
    api_url = 'https://www.eloquii.com/on/demandware.store/Sites-eloquii-Site/default/Product-GetVariants?'

    currency = 'USD'
    gender = 'women'


class EloquiiParser(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    description_css = ".description.pt-3 li:first-child ::text"
    care_css = '.description.pt-3 li:not(:first-child) ::text'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)
        if not garment:
            return
        self.boilerplate_normal(garment, response)
        garment['gender'] = self.gender
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = {}
        garment['meta'] = {'requests_queue': self.request_variants(product_id)}
        return self.next_request_or_garment(garment)

    def parse_variants(self, response):
        garment = response.meta['garment']
        variants = json.loads(response.text)
        return self.process_skus_data(variants['variations']['variants'], garment)

    def request_variants(self, product_id):
        url = add_or_replace_parameter(self.api_url, 'pid', product_id)
        url = add_or_replace_parameter(url, 'format', 'ajax')
        return [Request(url, self.parse_variants)]

    @staticmethod
    def product_id(response):
        return clean(response.css('.yotpo.yotpo-pictures-widget::attr(data-product-id)'))[0]

    @staticmethod
    def product_category(response):
        return clean(response.css('.breadcrumb.bg-white .text-12::text'))

    @staticmethod
    def product_name(response):
        return clean(response.xpath('//meta[@name="keywords"]/@content'))[0]

    def image_urls(self, response):
        image_urls = []
        images = clean(response.xpath('//script[contains(text(),"app.execUjs")]/text()'))[0]
        image_sets = re.findall('("xlarge"\s*:\s*\[.*?\])', images)
        for image_set in image_sets:
            images = json.loads("{" + image_set + "}")
            for image in images['xlarge']:
                image_urls.append(response.urljoin(image['url']))
        return image_urls

    def process_skus_data(self, variants, garment):
        for variant in variants:

            if type(variant) is not dict:
                for fit in variant:
                    garment['skus'].update(self.skus(fit))
            else:
                garment['skus'].update(self.skus(variant))

        return self.next_request_or_garment(garment)

    def skus(self, variant):
        money_strs = [variant['pricing']['sale'], variant['pricing']['standard'], self.currency]
        sku = self.product_pricing_common(None, money_strs=money_strs)
        sku['colour'] = variant['attributes']['colorCode']

        size = self.one_size if variant['size'] == 'NS' else variant['size']
        sku['size'] = f"{size}_{variant['sizeType']}"

        sku['out_of_stock'] = not variant['inStock']
        sku_id = f"{sku['colour']}_{sku['size']}"
        return {sku_id: sku}


class EloquiiCrawler(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = EloquiiParser()
    listing_css = [
        '.sub-nav-style a',
        '.justify-content-center.mt-5 div:nth-child(3) a'
    ]
    product_css = ['.product-images a:first-child']

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse'
             ),
        Rule(
            LinkExtractor(restrict_css=product_css), callback='parse_item'
        )
    )
