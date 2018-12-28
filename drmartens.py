import json

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractor import LinkExtractor

from parse_item_structure import ParseItem
from helpers import extract_price_details


class ProductParser(scrapy.Spider):
    def __init__(self):
        self.seen_ids = set()

    def parse(self, response):
        item = ParseItem()
        retailer_sku = self.extract_id(response)

        if not self.is_new_item(retailer_sku):
            return item

        item['name'] = self.extract_name(response)
        item['retailer_sku'] = retailer_sku
        item['care'] = self.extract_care(response)
        item['url'] = response.url
        item['spider_name'] = 'drmartens_au'
        item['market'] = self.extract_market()
        item['retailer'] = self.extract_retailer()
        item['brand'] = self.extract_brand()
        item['category'] = self.extract_category(response)
        item['description'] = self.extract_description(response)
        item['image_urls'] = self.extract_image_urls(response)
        item['trail'] = response.meta.get('trail', [])
        item['skus'] = self.extract_skus(response)

        return item

    def is_new_item(self, retailer_sku):
        if retailer_sku and retailer_sku not in self.seen_ids:
            self.seen_ids.add(retailer_sku)
            return True

        return False

    def extract_id(self, response):
        return response.css('.extra-product::attr(data-sku)').extract_first()

    def extract_name(self, response):
        return response.css('.product-info-main .page-title span::text').extract_first()

    def extract_care(self, response):
        css = '.additional-attributes .large-4 .content-short-description p::text'
        care_content = response.css(css).extract()
        return [care.strip() for care in care_content if care.strip()]

    def extract_category(self, response):
        category = response.css('.breadcrumbs .item strong::text').extract_first()
        return [category.strip()] if category else []

    def extract_description(self, response):
        content = response.css('.additional-attributes .large-8 .content::text').extract_first()
        return [x.strip() for x in content.split('.') if x.strip()]

    def extract_image_urls(self, response):
        xpath = "//script[contains(., 'mage/gallery/gallery')]/text()"
        raw_image_urls = response.xpath(xpath).re('"data": (.*?}])')
        if raw_image_urls:
            raw_image_urls = [image['img'] for image in json.loads(raw_image_urls[0])]

        return raw_image_urls

    def extract_skus(self, response):
        skus = []
        xpath = "//script[contains(.,'sizeRangesSort')]/text()"
        price = response.xpath(xpath).re('"prices":({".*?"}})')[0]
        price = json.loads(price)
        product_price = extract_price_details([price['oldPrice']['amount'], price['finalPrice']['amount']])
        size_record = response.xpath(xpath).re('jsonConfig:{"attributes":({.*?}})')[0]
        size_record = json.loads(size_record)

        item = {}
        item['color'] = size_record['93']['options'][0]['label']
        item['currency'] = response.css('.price-final_price meta:nth-child(3)::attr(content)').extract_first()
        item.update(product_price)

        for option in size_record['243']['options']:
            size_option = item.copy()
            size_option['size'] = option['label']
            size_option['sku_id'] = f"{item['color']}_{option['label']}"
            if not option['products']:
                size_option['out_of_stockand'] = True
            skus.append(size_option)

        return skus

    def extract_market(self):
        return 'AU'

    def extract_retailer(self):
        return 'drmartens-au'

    def extract_brand(self):
        return 'Dr. Martens'


class DrmartensSpider(CrawlSpider):
    name = 'drmartens-crawl-spider'
    allowed_domains = ['www.drmartens.com.au']
    start_urls = ['http://www.drmartens.com.au/']
    product_parser = ProductParser()

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/71.0.3578.98 Safari/537.36'
    }

    listing_css = ['.column.main']
    product_css = ['.main-menu']
    rules = [
        Rule(LinkExtractor(restrict_css=product_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse_item')
    ]

    def parse(self, response):
        title = self.extract_title(response)
        trail = response.meta.get('trail', [])
        trail = trail + [[title, response.url]]

        for request in super().parse(response):
            request.meta['trail'] = trail.copy()
            yield request

    def parse_item(self, response):
        return self.product_parser.parse(response)

    def extract_title(self, response):
        title = response.css('title::text').extract_first()
        return title.split('|')[0] if title else title
