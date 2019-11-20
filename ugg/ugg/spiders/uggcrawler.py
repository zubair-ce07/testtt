import json
import re
from urllib.parse import urljoin

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule, Spider

from ..items import Product


class ProductParser(Spider):
    seen_ids = set()
    name = 'uggSpider'

    def parse(self, response):
        retailer_sku_id = self.product_retailer_sku(response)
        if retailer_sku_id in self.seen_ids:
            return

        self.seen_ids.add(retailer_sku_id)
        trail = response.meta.get('trail', [])
        trail.append(response.url)

        item = Product()
        item['retailer_sku'] = retailer_sku_id
        item['trail'] = trail
        item['gender'] = self.product_gender(response)
        item['category'] = self.product_category(response)
        item['brand'] = 'UGG'
        item['url'] = response.url
        item['market'] = 'AU'
        item['retailer'] = 'UGG-AU'
        item['name'] = self.product_name(response)
        item['description'] = self.product_description(response)
        item['images_url'] = self.product_images(response)
        item['skus'] = self.product_sku(response)
        item['price'] = self.product_price(response)
        item['currency'] = self.product_currency(response)
        item['meta'] = {'requests': self.product_sku_requests(response, item)}

        return self.next_item_or_request(item)

    def product_retailer_sku(self, response):
        sku_data = self.load_sku_data(response)
        return sku_data.get('displayCode')

    def product_name(self, response):
        return response.css('.product-name::text').get()

    def product_gender(self, response):
        gender = response.css('.product-spec-list dd::text').get()
        return gender if gender else 'unisex'

    def product_category(self, response):
        selector = '.breadcrumb-item:nth-child(n+2) a::attr(data-id)'
        return response.css(selector).getall()

    def product_description(self, response):
        selector = '.product-detail-card .card-text::text'
        raw_description = response.css(selector).get()
        return raw_description.strip()

    def product_currency(self, response):
        selector = '.prices [itemprop="priceCurrency"]::attr(content)'
        return response.css(selector).get()

    def product_price(self, response):
        selector = '.prices .value::attr(content)'
        return response.css(selector).get()

    def product_previous_price(self, response):
        selector = '.prices .strike-through span::attr(content)'
        return response.css(selector).get()

    def product_sku_requests(self, response, item):
        requests = []
        selector = '.color-value:not(.selected)::attr(data-attr-value)'
        product_sku_variants = response.css(selector).getall()

        for color_variant in product_sku_variants:
            url = re.sub(r'[A-Z]{3,}', color_variant, response.url)
            requests.append(
                Request(url=url, callback=self.add_product_skus, meta={'item': item})
            )
        return requests

    def add_product_skus(self, response):
        item = response.meta['item']
        item['images_url'] += self.product_images(response)
        item['skus'] += self.product_sku(response)
        return self.next_item_or_request(item)

    def product_images(self, response):
        raw_images = response.css('.product-detail-img::attr(data-json)').get()
        raw_images_content = json.loads(raw_images)
        large_sized_images = raw_images_content.get('large')
        return [img_item.get('url') for img_item in large_sized_images]

    def product_sku(self, response):
        skus = []
        sku_data = self.load_sku_data(response)
        product_sizes = self.product_sizes(response)

        for product_size in product_sizes:
            sku = {}
            sku['colour'] = sku_data.get('displayValue'),
            sku['previous_prices'] = [self.product_previous_price(response)],
            sku['size'] = product_size,
            sku['sku_id'] = self.product_retailer_sku(response)
            skus.append(sku)

        return skus

    def next_item_or_request(self, item):
        if item['meta']['requests']:
            request = item['meta']['requests'].pop()
            yield request
        else:
            item.pop('meta')
            yield item

    def load_sku_data(self, response):
        raw_data = response.css('.render-product-selected::attr(data-json)').get()
        return json.loads(raw_data)

    def product_sizes(self, response):
        selector = '.select-size option:not([disabled]):nth-child(n+2)::text'
        raw_sizes = response.css(selector).getall()
        return self.remove_extra_spaces(raw_sizes)

    def remove_extra_spaces(self, raw_text):
        clean_text = []
        for text_item in raw_text:
            clean_item = text_item.strip()
            if clean_item:
                clean_text.append(clean_item)
        return clean_text


class UggCrawler(CrawlSpider):
    name = 'ugg_crawler'
    product_parser = ProductParser()

    allowed_domains = ['au.ugg.com']
    start_urls = ['https://au.ugg.com']
    allow = r'/catalog/'
    listing_css = ('.btn-show-all',)
    cookies = {'NM()sdf': '905077ed-6e1f-27a1-1c38-95b01189b480;'}
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        'DOWNLOAD_DELAY': '5'
    }

    rules = (
        Rule(LinkExtractor(allow=allow, restrict_css=listing_css), callback='parse_listing'),
    )

    def start_requests(self):
        yield from [Request(url, cookies=self.cookies) for url in self.start_urls]

    def parse_listing(self, response):
        product_requests = response.css('.card-img a::attr(href)').getall()
        meta = {'trail': [response.url]}
        yield from [Request(url=urljoin(response.url, url), cookies=self.cookies, callback=self.product_parser.parse,
                            meta=meta) for url in product_requests]

        next_page_url = response.css('.show-more button::attr(data-url)').get()
        if not next_page_url:
            return
        yield Request(url=urljoin(response.url, next_page_url), cookies=self.cookies, callback=self.parse_listing)
