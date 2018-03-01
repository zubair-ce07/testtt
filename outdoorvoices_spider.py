import json
import re

from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseCrawlSpider, BaseParseSpider, clean
from ..parsers.jsparser import JSParser
from ..utils.decorators import remove_duplicates


class Mixin:
    retailer = "outdoorvoices-us"
    market = "US"
    allowed_domains = ["outdoorvoices.com"]
    start_urls = ["https://www.outdoorvoices.com/"]


class OutdoorVoicesParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + "-parse"
    price_css = 'meta[property="og:price:currency"]::attr(content)'

    def parse(self, response):
        product = self.raw_product(response)
        sku_id = self.product_id(product)
        garment = self.new_unique_garment(sku_id)

        if not garment:
            return

        self.boilerplate(garment, response)
        garment['name'] = self.product_name(response)
        garment['description'] = self.product_description(response)
        garment['brand'] = self.product_brand(response)
        garment['category'] = self.product_category(response)
        garment['image_urls'] = self.image_urls(product)
        garment['skus'] = self.skus(response, product)
        garment['merch_info'] = self.merch_info(response)
        garment['meta'] = {
            'requests_queue': self.description_request(response)
        }
        return self.next_request_or_garment(garment)

    def parse_description(self, response):
        garment = response.meta['garment']
        garment['care'] = self.product_care(response)
        garment['description'] += self.updated_description(response)
        return self.next_request_or_garment(garment)

    def raw_product(self, response):
        raw_product = response.xpath('//script[contains(text(),"shopify_product_data")]/text()').extract_first()
        return JSParser(raw_product)["shopify_product_data"]

    def product_id(self, product):
        return product["id"]

    def product_name(self, response):
        return clean(response.css('.product-hero__title ::text'))[0]

    def product_category(self, response):
        return response.css('script.analytics::text').re('category":"([\w+\s?]+)')

    def product_brand(self, response):
        return "Outdoor Voices"

    def product_description(self, response):
        raw_descriptions = clean(response.css('meta[property="og:description"]::attr(content)'))
        return self.clean_description(raw_descriptions)

    @remove_duplicates
    def product_care(self, response):
        raw_description = self.raw_description(response)
        return clean([rc for rc in raw_description if self.care_criteria_simplified(rc)])

    def merch_info(self, response):
        name = self.product_name(response)
        return ["Limited Edition"] if "limited edition" in name.lower() else []

    @remove_duplicates
    def image_urls(self, product):
        return [i["src"] for i in product["images"] if "facebook" not in i["src"]]

    def skus(self, response, product):
        sku_to_hide = product.get("metafields_admin").get("skus_to_hide", "").split()
        skus = {}
        for raw_sku in product["variants"]:
            if raw_sku["sku"] in sku_to_hide or not raw_sku['available']:
                continue
            sku = self.product_pricing_common_new(response,
                                                  money_strs=[raw_sku['price'],
                                                              raw_sku['compare_at_price']],
                                                  is_cents=True)
            sku['colour'] = raw_sku['option1']
            sku['size'] = self.one_size if raw_sku['option2'] == 'OS' else raw_sku['option2']
            sku_id = f'{sku["colour"]}_{sku["size"]}'
            skus[sku_id] = sku
        return skus

    def description_request(self, response):
        resource_id = response.css('script#__st::text').re('rid\":(\d+)')[0]
        url = f'https://mainframe.outdoorvoices.com/api/v2/product/{resource_id}/'
        return [Request(url=url, callback=self.parse_description)]

    @remove_duplicates
    def clean_description(self, raw_descriptions):
        return sum([re.split('[\.\s]', rd) for rd in raw_descriptions], [])

    def updated_description(self, response):
        raw_description = self.raw_description(response)
        return clean([rc for rc in raw_description if not self.care_criteria_simplified(rc)])

    def raw_description(self, response):
        raw_descriptions_html = [rdh["body"] for rdh in json.loads(response.text)["copy"]]
        raw_description = sum(
            [self.text_from_html(rd) for rd in raw_descriptions_html], [])
        return self.clean_description(raw_description)


class OutdoorVoicesCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + "-crawl"
    parse_spider = OutdoorVoicesParseSpider()

    listings_w_css = ['#women-dropdown']
    listings_m_css = ['#men-dropdown']

    products_css = ['.collection-variant__title-wrap']

    deny = ['gift-certificate']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_w_css, deny=deny), callback='parse_and_add_women'),
        Rule(LinkExtractor(restrict_css=listings_m_css, deny=deny), callback='parse_and_add_men'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )

    def parse(self, response):
        yield from super().parse(response)
        resource_id = response.css('script#__st::text').re('rid\":(\d+)')[0]
        url = f'https://mainframe.outdoorvoices.com/api/v2/collection/{resource_id}/'
        response.meta['trail'] = self.add_trail(response)
        yield Request(url=url, meta=response.meta.copy(), callback=self.parse_categories)

    def parse_categories(self, response):
        for product in json.loads(response.text)["product_bundles"]:
            if product["swatches"]:
                url = product["swatches"][0]["shopify_path"]
                yield Request(url=url, meta=response.meta.copy(), callback=self.parse_spider.parse)

