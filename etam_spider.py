import json
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = "etam-cn"
    market = 'CN'
    lang = 'zh'
    gender = 'women'
    allowed_domains = ['etam.com.cn']
    start_urls = ['http://www.etam.com.cn/']
    custom_settings = {'DOWNLOAD_DELAY': 1}


class EtamParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + "-parse"
    price_css = "div.normal-price ::text"

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)
        if not garment:
            return
        self.boilerplate_normal(garment, response)
        garment['skus'] = self.skus(response, garment)
        garment['image_urls'] = self.image_urls(response)
        garment['merch_info'] = self.merch_info(response)
        return self.next_request_or_garment(garment)

    def skus(self, response, garment):
        skus = {}
        common = self.product_pricing_common_new(response)
        common['colour'] = ""
        sizes = {}
        sizes_script = response.css('div.option-panel script').extract_first()
        raw_sizes = re.findall('"options":(.*)}},"template"', sizes_script)[0]
        raw_stock = re.findall('stockProducts = {(.*)};', sizes_script)[0]
        raw_stock = "{" + raw_stock + "}"
        json_stock = json.loads(raw_stock)
        json_sizes = json.loads(raw_sizes)
        for size in json_sizes:
            sizes[size["label"].replace("\\", "")] = size["products"][0]
        for variant_key, variant_value in sizes.items():
            sku = common.copy()
            sku['size'] = variant_key
            if not json_stock[variant_value]["has_stock"]:
                sku['out_of_stock'] = True
            skus[sku['size']] = sku
        return skus

    def raw_brand_and_id(self, response):
        return clean(response.css('div.product-name > h1 ::text'))

    def product_id(self, response):
        return self.raw_brand_and_id(response)[1]

    def product_brand(self, response):
        return self.raw_brand_and_id(response)[0]

    def product_name(self, response):
        return clean(response.css('p.info-name ::text'))

    def product_description(self, response):
        return ""

    def product_care(self, response):
        return ""

    def product_category(self, response):
        return clean(response.css('div.breadcrumbs a ::text'))

    def image_urls(self, response):
        return clean(response.css('a[id="zoomGalery"]::attr(href)'))

    def merch_info(self, response):
        return "".join(clean(response.css('div.member-price ::text')))


class EtamCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + "-crawl"
    parse_spider = EtamParseSpider()

    products_css = '.products-grid'

    deny = [
        '/vip',
        '/store_map',
        'http://www.etam.com'
    ]

    listing_css = [
        '.main-navi-list',
        '.toolbar-bottom .pages'
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css, deny=deny), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )
