import json

import re
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean


class EloquiiMixin:
    retailer = 'eloquii-us'

    allowed_domains = ['www.eloquii.com']
    start_urls = [
        'https://www.eloquii.com/',
    ]
    one_sizes = ["One Size", "NS"]

    default_brand = "ELOQUII"
    market = "US"
    gender = 'women'
    details_url_t = 'https://www.eloquii.com' \
                    '/on/demandware.store/Sites-eloquii-Site/default/Product-GetVariants?pid={}&format=json'


class EloquiiParseSpider(BaseParseSpider, EloquiiMixin):
    name = EloquiiMixin.retailer + '-parse'

    raw_description_css = ".productdetailcolumn .description ::text"
    brand_css = '.el_header_logo::attr(title)'

    def parse(self, response):
        pid = self.product_id(response)
        garment = self.new_unique_garment(pid)

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment["skus"] = {}
        garment["image_urls"] = self.product_images(response)
        garment["merch_info"] = self.merch_info(response)

        if self.product_availability(response):
            garment["out_of_stock"] = True

            return garment

        garment['meta'] = {'requests_queue': self.details_requests(response, pid)}
        return self.next_request_or_garment(garment)

    def details_requests(self, response, pid):
        currency = self.currency(response)
        return [Request(url=self.details_url_t.format(pid), meta={"currency": currency}, callback=self.parse_skus)]

    def parse_skus(self, response):
        garment = response.meta["garment"]
        garment["skus"].update(self.skus(response))

        return self.next_request_or_garment(garment)

    def skus(self, response):
        skus = {}
        currency = response.meta["currency"]
        raw_details = json.loads(response.text)

        for detail in raw_details["variations"]["variants"]:
            stock_available = detail["inStock"]

            if not stock_available:
                continue

            price = detail["pricing"]["standard"]
            p_price = detail["pricing"]["sale"]
            sku = self.product_pricing_common(None, money_strs=[price, p_price, currency])

            sku["colour"] = detail['attributes']['colorCode']
            size = detail['attributes'].get('size')
            sku['size'] = size if size and size not in self.one_sizes else self.one_size
            size_type = detail['attributes'].get('sizeType')
            length = detail['attributes'].get('pantLength')

            if size_type and length:
                sku['size'] = f'{size}_{size_type}_{length}'

            elif size_type:
                sku['size'] = f'{size}_{size_type}'

            elif length:
                sku['size'] = f'{size}_{length}'

            skus[f'{sku["colour"]}_{sku["size"]}'] = sku

        return skus

    def currency(self, response):
        return clean(response.css('[property="og:price:currency"]::attr(content)'))[0]

    def product_id(self, response):
        return clean(response.css('.riifavorites a::attr(rel)'))[0]

    def product_name(self, response):
        return clean(response.css('[itemprop="name"]::text'))[0]

    def product_category(self, response):
        return clean(response.css('[itemprop="title"]::text'))[:-1]

    def product_availability(self, response):
        return clean(response.xpath('//*[contains(text(), "Coming Soon") or contains(text(), "Sold Out")]'))

    def product_images(self, response):
        script = clean(response.xpath('//script[contains(text(),"masterID")]/text()'))[0]
        image_urls = re.findall('url"\s?:\s?"(.*?)"', script)
        return list(set([response.urljoin(url) for url in image_urls if "xlarge" in url]))

    def merch_info(self, response):
        raw_info = clean(response.xpath('//*[contains(text(),"Is Coming Soon")]'))
        return ["Coming Soon"] if raw_info else ''


class EloquiiCrawlSpider(BaseCrawlSpider, EloquiiMixin):
    name = EloquiiMixin.retailer + '-crawl'
    parse_spider = EloquiiParseSpider()

    listings_css = [
        "#nav_menu .d-flex",
        ".col-auto.pt-1"

    ]
    product_css = '.product-images'

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')
    )
