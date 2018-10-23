import re
import json
import scrapy

from orsay.items import Product
from scrapy.exceptions import DropItem
from w3lib.url import url_query_cleaner
from scrapy.spiders import CrawlSpider, Rule, Spider
from scrapy.linkextractors import LinkExtractor


class ProductParser(Spider):
    name = 'orsay-parser'
    sku_id_format = '{}_{}'
    ids_seen = set()

    def parse(self, response):
        if self.product_id(response) in self.ids_seen:
            return
        else:
            self.ids_seen.add(self.product_id(response))
            product = Product()
            product['brand'] = 'orsay'
            product['care'] = self.product_care(response)
            product['category'] = self.product_category(response)
            product['description'] = self.product_description(response)
            product['image_urls'] = self.product_image_urls(response)
            product['retailer_sku'] = self.product_id(response)
            product['name'] = self.product_name(response)
            product['skus'] = self.product_sku(response)
            product['url'] = response.url
            product['meta'] = {'requests': self.product_colors_requests(
                response, product)}

            return self.next_request_or_item(product)

    def parse_colors(self, response):
        item = response.meta['item']
        item['skus'].update(self.product_sku(response))
        item['image_urls'] += self.product_image_urls(response)

        return self.next_request_or_item(item)

    def next_request_or_item(self, item):
        color_requests = item['meta']['requests']
        if color_requests:
            req = color_requests.pop()
            yield req
        else:
            item.pop('meta')
            yield item

    def product_sku(self, response):
        sizes = self.product_size(response)
        skus = {}

        common_sku = {}
        common_sku['price'] = int(self.product_price(response))
        common_sku['previous_prices'] = self.product_previous_price(response)
        common_sku['colour'] = self.product_selected_color(response)
        common_sku['currency'] = self.product_currency(response)

        if sizes:
            for size in sizes:
                size = size.strip()
                sku = common_sku.copy()
                sku['size'] = size
                sku_id = self.sku_id_format.format(common_sku['colour'], size)
                skus[sku_id] = sku
        else:
            sku_id = self.sku_id_format.format(
                common_sku['colour'], 'One Size')
            skus[sku_id] = common_sku.copy()

        return skus

    def product_care(self, response):
        return response.css('.product-material p::text').extract()

    def product_category(self, response):
        return response.css('.breadcrumb a:nth-child(n+3) span::text').extract()

    def product_description(self, response):
        css = '.with-gutter::text, .product-info-title + div::text'
        raw_discription = response.css(css).extract()
        discriptions = [re.sub('[-\n]', '', discription)
                        for discription in raw_discription]
        return [discription for discription in discriptions if discription != '']

    def product_image_urls(self, response):
        raw_image_urls = response.css('.productthumbnail::attr(src)').extract()
        return [url_query_cleaner(image_url) for image_url in raw_image_urls]

    def product_name(self, response):
        return response.css('.product-name::text').extract_first()

    def product_color(self, response):
        colors = []
        css = '.swatches color a::attr(title)'

        for item in response.css(css).extract():
            colors.append(item.split('-')[-1])
        return colors

    def product_selected_color(self, response):
        return response.css('.selected-value::text').extract_first()

    def product_currency(self, response):
        return response.css('.country-currency::text').extract_first()

    def product_price(self, response):
        raw_price = response.css('.product-price span::text').extract_first()
        price = re.sub('[,€\n\r\t]', '', raw_price)
        return price

    def product_previous_price(self, response):
        css = '.product-price .price-standard::text'
        raw_prices = response.css(css).extract()
        prices = [re.sub('[,€\n\t\r]', '', price) for price in raw_prices]
        return [int(price) for price in prices if price != '']

    def product_size(self, response):
        css = '.size li.selectable a::text'
        return response.css(css).extract()

    def sku_id(self, response):
        raw_data = self.extract_raw_data(response)
        return raw_data['idListRef12']

    def product_colors_requests(self, response, item):
        css = '.color li:not(.selected) a::attr(href)'
        links = response.css(css).extract()
        return [scrapy.Request(link, callback=self.parse_colors,
                               meta={'item': item}, dont_filter=True) for link in links]

    def product_id(self, response):
        data = self.extract_raw_data(response)
        return data['idListRef6']

    def extract_raw_data(self, response):
        css = '.js-product-content-gtm::attr(data-product-details)'
        data = response.css(css).extract_first()
        return json.loads(data)

    def extract_total_items(self, response):
        css = '[class*=pagination-product-count]::attr(data-count)'
        return response.css(css).extract_first()

    def extract_shown_items(self, response):
        css = '.load-more-progress-label span::text'
        return response.css(css).extract_first()
