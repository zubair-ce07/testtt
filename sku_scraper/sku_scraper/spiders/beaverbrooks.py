# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from ..items import Item
from ..utilities import pricing


class BeaverBrooksParseSpider(Spider):
    name = 'beaverbrooks-parse'
    size_request_t = 'https://www.beaverbrooks.co.uk/ajax/productDetails?productCode={}'

    allowed_domains = ['beaverbrooks.co.uk']

    def parse(self, response):
        item = Item()
        item['retailer_sku'] = self.extract_retailer_sku(response)
        item['name'] = self.extract_name(response)
        item['image_urls'] = self.extract_image_urls(response)
        item['care'] = self.extract_care(response)
        item['description'] = self.extract_description(response)
        item['category'] = self.extract_category(response)
        item['url'] = self.extract_product_url(response)

        item['skus'] = {}
        item['meta'] = {}

        item['meta']['requests'] = self.create_size_requests(response)
        if not item['meta']['requests']:
            item['skus'].update(self.extract_sku(response))

        yield self.generate_request_or_item(item)

    def parse_size_request(self, response):
        item = response.meta['item']
        item['skus'].update(self.extract_sku(response))

        return self.generate_request_or_item(item)

    def create_size_requests(self, response):
        size_codes = self.extract_size_codes(response)

        return [Request(self.size_request_t.format(size_code),
                        callback=self.parse_size_request) for size_code in size_codes]

    def generate_request_or_item(self, item):
        if item['meta'].get('requests'):
            request = item['meta']['requests'].pop()
            request.meta['item'] = item
            return request

        del item['meta']
        return item

    def extract_size_codes(self, response):
        css = 'form.form-select option:not([disabled="disabled"])::attr(value)'
        return response.css(css).extract()

    def extract_retailer_sku(self, response):
        css = 'meta[itemprop="sku"]::attr(content)'
        return response.css(css).extract()

    def extract_name(self, response):
        css = 'span#productName::text'
        return response.css(css).extract_first()

    def extract_brand(self, response):
        css = 'span[itemprop="brand"] > meta::attr(content)'
        return response.css(css).extract()

    def extract_image_urls(self, response):
        css = 'a.product-gallery__thumb img::attr(src), div.product-image img::attr(src)'
        return response.css(css).extract()

    def extract_description(self, response):
        css = 'p[itemprop="description"]::text, p[itemprop="description"] ~ p::text'
        return response.css(css).extract()

    def extract_category(self, response):
        trail = response.meta.get('trail') or []
        return [link_text for link_text, _ in trail if link_text and not link_text.isdigit()]

    def extract_product_url(self, response):
        css = 'meta[itemprop="url"]::attr(content)'
        return response.css(css).extract()

    def extract_care(self, response):
        care_key_css = 'table.product-specification td.attrib::text'
        care_value_css = 'table.product-specification td:not(.attrib)::text'
        raw_care_keys = response.css(care_key_css).extract()
        raw_care_values = [value.strip()
                           for value in response.css(care_value_css).extract()]

        return [key + ': ' + value for key, value in zip(raw_care_keys, raw_care_values)]

    def extract_money_strings(self, response):
        css = 'span[itemprop="price"]::attr(content), p.prod-price-was::text'
        return response.css(css).extract()

    def extract_currency(self, response):
        css = 'span[itemprop="priceCurrency"]::attr(content)'
        return response.css(css).extract_first()

    def check_availability(self, response):
        css = 'div#productStockCheckAvailability'
        return response.css(css).extract()

    def extract_sku(self, response):
        sku = pricing(self.extract_money_strings(response))

        if 'ajax' in response.url:
            size = response.url[-3:] if response.url[-1].isdigit() else response.url[-1]
        else:
            size = 'One Size'

        sku['size'] = size
        sku['currency'] = self.extract_currency(response)

        if not self.check_availability(response):
            sku['out_of_stock'] = True

        return {size: sku}


class BeaverBrooksCrawlSpider(CrawlSpider):
    name = 'beaverbrooks-crawl'

    allowed_domains = ['beaverbrooks.co.uk']
    start_urls = ['https://www.beaverbrooks.co.uk/']

    deny = ['accessories', 'favourites', 'gift']

    listings_css = ['div.main-nav__category', 'ul.list-pagination']
    products_css = ['div.product-list__item']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css, deny=deny), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_product'),
    )

    product_parser = BeaverBrooksParseSpider()

    def parse(self, response):
        for request_or_item in super().parse(response):
            if isinstance(request_or_item, Request):
                request_or_item.meta['trail'] = self.make_trail(response)
            yield request_or_item

    def parse_product(self, response):
        yield from self.product_parser.parse(response)

    def make_trail(self, response):
        link_text = response.meta.get('link_text') or ''
        return (response.meta.get('trail') or []) + [(link_text.strip(), response.url)]
