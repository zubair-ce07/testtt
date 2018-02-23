import json
import re

from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseCrawlSpider, BaseParseSpider, clean


class Mixin:
    retailer = "outdoorvoices-us"
    market = "US"
    allowed_domains = ["outdoorvoices.com"]
    start_urls = ["https://www.outdoorvoices.com/"]


class OutdoorVoicesParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + "-parse"

    def parse(self, response):
        sku_id = self.product_id(response)
        garment = self.new_unique_garment(sku_id)

        if not garment:
            return

        self.boilerplate(garment, response)
        garment['name'] = self.product_name(response)
        garment['description'] = self.product_description(response)
        garment['brand'] = self.product_brand(response)
        garment['category'] = self.product_category(response)
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response)
        garment['merch_info'] = self.merch_info(response)
        garment['meta'] = {
            'requests_queue': self.care_request(response)
        }
        return self.next_request_or_garment(garment)

    def product_id(self, response):
        return response.css('.wrap script:first-of_type::text').re('id:\s?(\d+)')[0]

    def product_name(self, response):
        return response.css('.product-hero__title ::text').extract_first()

    def product_category(self, response):
        return response.css('script.analytics::text').re('category":"([\w+\s?]+)')

    def product_brand(self, response):
        return response.css('script.analytics::text').re('brand":"([\w+\s?]+)')

    def product_description(self, response):
        return clean(response.css('meta[property="og:description"]::attr(content)'))

    def image_urls(self, response):
        return re.findall('src:\s?\"(.+?)\"',
                          response.css('.wrap script:first-of_type::text').re('images:\s?(\[.+\])')[0])

    def skus(self, response):
        raw_skus = json.loads(response.css('.wrap script:first-of_type::text').re('variants:\s?(\[.+\])')[0])
        currency = response.css('script.analytics::text').re('currency":"(\w+)')[0]
        skus = {}
        for raw_sku in raw_skus:
            sku = self.product_pricing_common_new(response,
                                                  money_strs=[raw_sku['price'], currency, raw_sku['compare_at_price']],
                                                  is_cents=True)
            sku['colour'] = raw_sku['option1']
            sku['size'] = self.one_size if raw_sku['option2'] == 'OS' else raw_sku['option2']
            if not raw_sku['available']:
                sku['out_of_stock']: True
            sku_id = f'{sku["colour"]}_{sku["size"]}'.replace(' ', '')
            skus[sku_id] = sku
        return skus

    def care_request(self, response):
        resource_id = response.css('script#__st::text').re('rid\":(\d+)')[0]
        url = f'https://mainframe.outdoorvoices.com/api/v2/product/{resource_id}/'
        return [Request(url=url, callback=self.parse_care)]

    def parse_care(self, response):
        garment = response.meta['garment']
        care, description = self.product_care(response)
        garment['care'] = clean(care)
        garment['description'] += clean(description)
        return self.next_request_or_garment(garment)

    def product_care(self, response):
        care, description = [], []
        raw_cares_html = set([raw_content["body"] for raw_content in json.loads(response.text)["copy"]])
        for raw_care_html in raw_cares_html:
            raw_cares = self.text_from_html(raw_care_html)
            for raw_care in raw_cares:
                if self.care_criteria_simplified(raw_care):
                    care.append(raw_care)
                else:
                    description.append(raw_care)
        return care, description

    def merch_info(self, response):
        name = self.product_name(response)
        return ["Limited Edition"] if "limited edition" in name.lower() else []


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

    def parse_and_add_women(self, response):
        yield self.categories_request(response, 'women')

    def parse_and_add_men(self, response):
        yield self.categories_request(response, 'men')

    def categories_request(self, response, gender):
        resource_id = response.css('script#__st::text').re('rid\":(\d+)')[0]
        url = f'https://mainframe.outdoorvoices.com/api/v2/collection/{resource_id}/'
        meta = {'trail': self.add_trail(response), 'gender': gender}
        return Request(url=url, meta=meta, callback=self.parse_categories)

    def parse_categories(self, response):
        for product in json.loads(response.text)["product_bundles"]:
            if product["swatches"]:
                url = product["swatches"][0]["shopify_path"]
                yield Request(url=url, meta=response.meta.copy(), callback=self.parse_spider.parse)

