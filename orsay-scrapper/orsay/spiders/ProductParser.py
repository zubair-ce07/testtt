import re
import json
import scrapy

from orsay.items import OrsayItem
from scrapy.spiders import CrawlSpider, Rule, Spider
from scrapy.linkextractors import LinkExtractor


class ProductParser(Spider):
    name = 'orsay-parse'

    def parse(self, response):

        product = OrsayItem()

        product['brand'] = 'orsay'
        product['care'] = self.product_care(response)
        product['category'] = self.product_category(response)
        product['description'] = self.product_description(response)
        product['image_urls'] = self.product_image_urls(response)
        product['retailer_sku'] = self.product_id(response)
        product['name'] = self.product_name(response)
        product['skus'] = self.product_sku(response)
        product['url'] = response.url
        product['meta'] = self.product_colors_requests(
            response, product)
        return self.next_request_or_item(product)

    def parse_colors(self, response):
        item = response.meta['item']
        item['skus'].update(self.product_sku(response))
        item['image_urls'] += self.product_image_urls(response)

        return self.next_request_or_item(item)

    def next_request_or_item(self, item):
        color_requests = item['meta']
        if color_requests:
            req = color_requests.pop()
            yield req
        else:
            item.pop('meta')
            yield item

    def product_sku(self, response):
        sizes = self.product_size(response)
        skus = {}

        single_item = {}
        single_item['price'] = self.product_price(response)
        single_item['color'] = self.product_selected_color(response)
        single_item['currency'] = self.product_currency(response)

        for size in sizes:
            size = size.strip()
            sku = single_item.copy()
            sku['size'] = size
            unique_id = size + "_" + self.product_selected_color(response)

            skus.update({unique_id: sku})

        return skus

    def product_care(self, response):
        css = '.product-material p::text'
        return response.css(css).extract()

    def product_category(self, response):
        css = '.breadcrumb a span::text'
        return response.css(css).extract()

    def product_description(self, response):
        css = '.with-gutter::text, .product-info-title + div::text'
        data = response.css(css).extract()
        data = [re.sub('[-\n]', '', item) for item in data]
        return data

    def product_image_urls(self, response):
        css = '.productthumbnail::attr(src)'
        return response.css(css).extract()

    def product_name(self, response):
        css = '.product-name::text'
        return response.css(css).extract_first()

    def product_color(self, response):
        colors = []
        css = '.swatches color a::attr(title)'

        for item in response.css(css).extract():
            colors.append(item.split('-')[-1])
        return colors

    def product_selected_color(self, response):
        css = '.selected-value::text'
        return response.css(css).extract_first()

    def product_currency(self, response):
        css = '.country-currency::text'
        return response.css(css).extract_first()

    def product_price(self, response):
        css = '.product-price span::text'
        price = response.css(css).extract_first()
        replaced = re.sub('[,€]', '', price)
        return replaced.strip()

    def product_size(self, response):
        css = '.size li.selectable a::text'
        size = response.css(css).extract()
        return size

    def sku_id(self, response):
        data = self.extract_raw_data(response)
        return data['idListRef12']

    def product_colors_requests(self, response, item):
        xpath = '//ul[contains(@class, "swatches color")]/'\
            + 'li[not(contains(@class, "selected"))]//a/@href'
        links = response.xpath(xpath).extract()
        requests = [scrapy.Request(link, callback=self.parse_colors, meta={
                                   'item': item}) for link in links]

        return requests

    def product_id(self, response):
        data = self.extract_raw_data(response)
        return data['idListRef6']

    def extract_raw_data(self, response):
        css = '.js-product-content-gtm::attr(data-product-details)'
        data = response.css(css).extract_first()
        data = json.loads(data)
        return data
