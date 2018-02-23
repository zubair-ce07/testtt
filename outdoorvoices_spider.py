from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseCrawlSpider, BaseParseSpider, clean
import re
from json import loads

class Mixin:
    retailer = "outdoorvoices"
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
            'requests_queue' : self.care_request(response, garment)
        }
        return self.next_request_or_garment(garment)

    def product_id(self, response):
       return response.css('script::text').re('id:\s?(\d+)')[0]

    def product_name(self, response):
        return response.css('.product-hero__title ::text').extract_first()

    def product_category(self, response):
        return response.css('script::text').re('category":"([\w+\s?]+)')

    def product_brand(self, response):
        return response.css('script::text').re('brand":"([\w+\s?]+)')

    def product_description(self, response):
        return clean(response.css('meta[property="og:description"]::attr(content)'))

    def image_urls(self, response):
        raw_image_urls = response.css('script::text').re('images:\s?(\[.+\])')[0]
        return re.findall('src:\s?\"(.+?)\"', raw_image_urls)

    def skus(self, response):
        raw_skus = loads(response.css('script::text').re('variants:\s?(\[.+\])')[0])
        currency = response.css('script::text').re('currency":"(\w+)')[0]
        skus = {}
        for raw_sku in raw_skus:
            sku = {
                'price': raw_sku['price'],
                'currency': currency,
                'colour': raw_sku['option1'],
                'size': raw_sku['option2'],
            }
            if not raw_sku['available']:
                sku['out_of_stock']: True
            if raw_sku['compare_at_price']:
                sku['previous_prices'] = [raw_sku['compare_at_price']]
            sku_id = f'{sku["colour"]}_{sku["size"]}'.replace(' ','')
            skus[sku_id] = sku
        return skus

    def care_request(self, response, garment):
        resource_id = response.css('script::text').re('rid\":(\d+)')[0]
        url = f'https://mainframe.outdoorvoices.com/api/v2/product/{resource_id}/'
        return [Request(url=url, callback=self.parse_care)]

    def parse_care(self, response):
        garment = response.meta['garment']
        garment['care'] = clean(self.care(response))
        return self.next_request_or_garment(garment)

    def care(self, response):
        text = loads(response.text)
        care = []
        for raw_care in text["copy"]:
            if raw_care["title"] == "Details":
                if self.care_criteria_simplified(raw_care["body"]):
                    care.append(raw_care["body"])
                break
        for raw_care in text["copy"]:
            if raw_care["title"] == "The Technical":
                if self.care_criteria_simplified(raw_care["body"]):
                    care.append(raw_care["body"])
                break
        return care

    def merch_info(self, response):
        name = self.product_name(response)
        return [name] if "limited edition" in name.lower() else []


class OutdoorVoicesCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + "-crawl"
    parse_spider = OutdoorVoicesParseSpider()

    listings_w_css = ['#women-dropdown']
    listings_m_css = ['#men-dropdown']

    products_css = ['.collection-variant__title-wrap']

    deny = ['gift-certificate']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_w_css, deny=deny), callback='parse_women_page'),
        Rule(LinkExtractor(restrict_css=listings_m_css, deny=deny), callback='parse_men_page'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )

    def parse_women_page(self, response):
        yield self.collection_request(response, 'women')

    def parse_men_page(self, response):
        yield self.collection_request(response, 'men')

    def collection_request(self, response, gender):
        resource_id = response.css('script::text').re('rid\":(\d+)')[0]
        url = f'https://mainframe.outdoorvoices.com/api/v2/collection/{resource_id}/'
        meta = {'trail': self.add_trail(response), 'gender': gender}
        return Request(url=url, meta=meta, callback=self.parse_collection)

    def parse_collection(self, response):
        product_requests = self.product_requests(response)
        for request in product_requests:
            yield request

    def product_requests(self, response):
        text = loads(response.text)
        product_requests = []
        for item in text["product_bundles"]:
            if item["swatches"]:
                url = item["swatches"][0]["shopify_path"]
                product_requests.append(Request(url=url, meta=response.meta, callback=self.parse_spider.parse))
        return product_requests