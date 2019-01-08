import json

from scrapy import Spider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractor import LinkExtractor

from item_structure import Item
from helpers import extract_price_details


class ProductParser(Spider):
    def __init__(self):
        self.seen_ids = set()

    def parse(self, response):
        item = Item()
        retailer_sku = self.extract_id(response)

        if not self.is_new_item(retailer_sku):
            return

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
        raw_care = response.css(css).extract()
        return [care.strip() for care in raw_care if care.strip()]

    def extract_category(self, response):
        raw_category = response.css('.breadcrumbs .item strong::text').extract()
        return [category.strip() for category in raw_category]

    def extract_description(self, response):
        description = response.css('.additional-attributes .large-8 .content::text').extract_first()
        return [des.strip() for des in description.split('.') if des.strip()]

    def extract_image_urls(self, response):
        xpath = "//script[contains(., 'mage/gallery/gallery')]/text()"
        raw_image_urls = response.xpath(xpath).re_first('"data": (.*?}])')
        if raw_image_urls:
            raw_image_urls = [image['img'] for image in json.loads(raw_image_urls)]

        return raw_image_urls

    def extract_skus(self, response):
        skus = []
        common_sku = extract_price_details(self.extract_price(response))
        raw_skus = self.extract_raw_skus(response)
        common_sku['colour'] = raw_skus['93']['options'][0]['label']

        for raw_sku in raw_skus['243']['options']:
            sku = common_sku.copy()
            sku['size'] = raw_sku['label']
            sku['sku_id'] = f"{common_sku['colour']}_{raw_sku['label']}"
            if not raw_sku['products']:
                sku['out_of_stock'] = True
            skus.append(sku)

        return skus

    def extract_market(self):
        return 'AU'

    def extract_price(self, response):
        return response.css('.price-container .price::text').extract()

    def extract_retailer(self):
        return 'drmartens-au'

    def extract_currency(self, response):
        return response.css('.price-final_price meta::attr(content)').extract()[1]

    def extract_brand(self):
        return 'Dr. Martens'

    def extract_raw_skus(self, response):
        xpath = "//script[contains(.,'sizeRangesSort')]/text()"
        pattern = 'jsonConfig:{"attributes":({.*?}})'
        raw_skus = response.xpath(xpath).re_first(pattern)
        return json.loads(raw_skus)


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
        return title.split('|')[0] or None
