import json
import scrapy

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractor import LinkExtractor

from parse_item_structure import ParseItem
import helpers


class ProductParser(scrapy.Spider):
    def __init__(self):
        self.seen_ids = {}

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

        self.seen_ids[retailer_sku] = item

        return item

    def is_new_item(self, item):
        return item and item not in self.seen_ids

    def extract_id(self, response):
        return response.css('.extra-product::attr(data-sku)').extract_first()

    def extract_name(self, response):
        return response.css('.product-info-main .page-title span::text').extract_first()

    def extract_care(self, response):
        care_css = '.additional-attributes .large-4 .content-short-description p::text'
        care_content = response.css(care_css).extract()
        return [care.strip() for care in care_content if care.strip()]

    def extract_category(self, response):
        category = response.css('.breadcrumbs .item strong::text').extract_first()
        return [category.strip()] if category else []

    def extract_description(self, response):
        content = response.css('.additional-attributes .large-8 .content::text').extract_first()
        description = [x.strip() for x in content.split('.') if x.strip()]
        return description

    def extract_image_urls(self, response):
        image_urls = []
        xpath = "//script[contains(., 'mage/gallery/gallery')]/text()"
        images_data = response.xpath(xpath).re('"data": (.*?}])')
        if images_data:
            images_data = json.loads(images_data[0])
            image_urls = [image['img'] for image in images_data]

        return image_urls

    def extract_skus(self, response):
        skus = []
        xpath = "//script[contains(.,'sizeRangesSort')]/text()"
        path_record = response.xpath(xpath)
        price_record = path_record.re('"prices":{"oldPrice":({".*?"})')
        size_record = path_record.re('jsonConfig:{"attributes":({.*?}})')

        pattern = '.price-final_price meta::attr(content)'
        price_details = response.css(pattern).extract()
        product_price = helpers.extract_price_details(price_details, price_record)

        if not size_record:
            return size_record

        size_record = json.loads(size_record[0])
        size_options = {}
        for key in size_record:
            if size_record[key]['code'] == 'size':
                size_options['size'] = size_record[key]['options']
            else:
                size_options['color'] = size_record[key]['options']

        color = [x['label'] for x in size_options['color']]

        for option in size_options['size']:
            item = {}
            item['price'] = product_price['price']
            item['old_price'] = product_price['old_price']
            item['currency'] = product_price['currency']
            item['color'] = color[0]
            item['size'] = option['label']
            item['sku_id'] = f"{color[0]}_{option['label']}"

            if not option['products']:
                item['out_of_stockand'] = True

            skus.append(item)

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
            request.meta['trail'] = trail
            yield request

    def parse_item(self, response):
        return self.product_parser.parse(response)

    def extract_title(self, response):
        title = response.css('title::text').extract_first()
        return title.split('|')[0] if title else title
