import json

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
    spider_care = {'relaxed': [
        'soft', 'washed', 'preshrunk', 'stretch', 'smooth', 'slick', 'water resistant'
    ]}


class OutdoorVoicesParseSpider(Mixin, BaseParseSpider):
    name = Mixin.retailer + "-parse"
    price_css = 'meta[property="og:price:currency"]::attr(content)'

    def parse(self, response):
        raw_product = self.raw_product(response)
        sku_id = raw_product["id"]
        garment = self.new_unique_garment(sku_id)

        if not garment:
            return

        self.boilerplate(garment, response)
        garment['name'] = raw_product["title"]
        garment['description'] = raw_product["description"].split('. ')
        garment['brand'] = "Outdoor Voices"
        garment['category'] = self.product_category(response)
        garment['skus'] = self.skus(response, raw_product)
        garment['image_urls'] = self.image_urls(raw_product, garment['skus'])
        garment['merch_info'] = self.merch_info(raw_product)
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

    def product_category(self, response):
        return response.css('script.analytics::text').re('category":"([\w+\s?]+)')

    def merch_info(self, raw_product):
        return ["Limited Edition"] if "limited edition" in raw_product["description"].lower() else []

    @remove_duplicates
    def image_urls(self, product, skus):
        colors = [sku['colour'].lower() for id, sku in skus.items()]
        return [i["src"] for i in product["images"] if
                "facebook" not in i["src"] and any(clr in i['alt'].lower() for clr in colors)]

    def skus(self, response, product):
        sku_to_hide = product.get("metafields_admin").get("skus_to_hide", "").split()
        skus = {}
        for raw_sku in product["variants"]:
            if raw_sku["sku"] in sku_to_hide or not raw_sku['available']:
                continue
            money_strs = [raw_sku['price'], raw_sku['compare_at_price']]
            sku = self.product_pricing_common_new(response, money_strs=money_strs, is_cents=True)
            sku['colour'] = raw_sku['option1']
            sku['size'] = self.one_size if raw_sku['option2'] == 'OS' else raw_sku['option2']
            sku_id = f'{sku["colour"]}_{sku["size"]}'
            skus[sku_id] = sku
        return skus

    def product_care(self, response):
        return [rc for rc in self.raw_description(response) if self.care_criteria_simplified(rc)]

    def description_request(self, response):
        resource_id = response.css('script#__st::text').re('rid\":(\d+)')[0]
        url = f'https://mainframe.outdoorvoices.com/api/v2/product/{resource_id}/'
        return [Request(url=url, callback=self.parse_description)]

    def updated_description(self, response):
        return [rd for rd in self.raw_description(response) if not self.care_criteria_simplified(rd)]

    @remove_duplicates
    def raw_description(self, response):
        raw_desc = [rd["body"] for rd in json.loads(response.text)["copy"]]
        return clean(sum([desc.split('. ') for rd in raw_desc for desc in self.text_from_html(rd)], []))


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

