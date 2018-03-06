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

    def parse(self, response):
        raw_product = self.raw_product(response)
        sku_id = raw_product["id"]
        garment = self.new_unique_garment(sku_id)

        if not garment:
            return

        self.boilerplate(garment, response)
        garment['name'] = raw_product["title"]
        garment['description'] = self.product_description(response)
        garment['brand'] = "Outdoor Voices"
        garment['category'] = self.product_category(response)
        garment['merch_info'] = self.merch_info(raw_product)
        garment['meta'] = {
            'requests_queue': self.product_request(response, raw_product),
        }
        return self.next_request_or_garment(garment)

    def parse_product(self, response):
        garment = response.meta['garment']
        garment['care'] = self.product_care(response)
        garment['description'] += self.updated_description(response)
        garment['skus'] = self.skus(response)
        garment['image_urls'] = self.image_urls(response.meta['raw_images'], garment['skus'])
        return self.next_request_or_garment(garment)

    def raw_product(self, response):
        raw_product = response.xpath('//script[contains(text(),"shopify_product_data")]/text()').extract_first()
        return JSParser(raw_product)["shopify_product_data"]

    def product_category(self, response):
        return response.css('script.analytics::text').re('category":"([\w+\s?]+)')

    def product_description(self, response):
        return clean(response.css('meta[property="og:description"]::attr(content)').extract_first().split('. '))

    def merch_info(self, raw_product):
        return ["Limited Edition"] if "limited edition" in raw_product["description"].lower() else []

    @remove_duplicates
    def image_urls(self, images, skus):
        colors = [sku['colour'].lower() for sku_id, sku in skus.items()]
        return [i["src"] for i in images if
                "facebook" not in i["src"] and any(clr in i['alt'].lower() for clr in colors)]

    def skus(self, response):
        raw_product = json.loads(response.text)
        raw_variants = raw_product["variant_swatches"]
        variants = {var["swatch_id"]: var['color_attribute'] for v_id, var in raw_variants.items()}
        variants = [color for v_id, color in variants.items()]
        sku_to_hide = response.meta['sku_to_hide']
        sku_oos = response.meta['sku_oos']
        skus = {}
        for r_sku in raw_product["variants"]:
            if r_sku["sku"] in sku_to_hide or r_sku['sku'] in sku_oos or r_sku['color'] not in variants:
                continue
            money_strs = [r_sku['price'], r_sku['compare_at_price'], response.meta['currency']]
            sku = self.product_pricing_common_new(response, money_strs=money_strs)
            sku['colour'] = r_sku['color']
            sku['size'] = self.one_size if r_sku['size'] == 'OS' else r_sku['size']
            sku_id = f'{sku["colour"]}_{sku["size"]}'
            skus[sku_id] = sku
        return skus

    def product_care(self, response):
        return [rc for rc in self.raw_description(response) if self.care_criteria_simplified(rc)]

    def product_request(self, response, raw_product):
        resource_id = response.css('script#__st::text').re('rid\":(\d+)')[0]
        url = f'https://mainframe.outdoorvoices.com/api/v2/product/{resource_id}/'
        meta = {
            'sku_to_hide': self.sku_to_hide(raw_product),
            'raw_images': raw_product['images'],
            'sku_oos': self.sku_out_of_stock(raw_product),
            'currency': self.product_currency(response),
        }
        return [Request(url=url, callback=self.parse_product, meta=meta)]

    def updated_description(self, response):
        return [rd for rd in self.raw_description(response) if not self.care_criteria_simplified(rd)]

    @remove_duplicates
    def raw_description(self, response):
        raw_desc = [rd["body"] for rd in json.loads(response.text)["copy"]]
        return clean(sum([desc.split('. ') for rd in raw_desc for desc in self.text_from_html(rd)], []))

    def sku_to_hide(self, raw_product):
        return raw_product.get("metafields_admin").get("skus_to_hide", "").split()

    def sku_out_of_stock(self, raw_product):
        return [raw_sku['sku'] for raw_sku in raw_product["variants"] if not raw_sku['available']]

    def product_currency(self, response):
        return response.css('meta[property="og:price:currency"]::attr(content)').extract_first()


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

