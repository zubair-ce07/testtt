import json
import scrapy

from scrapy.spiders import CrawlSpider, Rule, Spider
from scrapy.linkextractors import LinkExtractor

from .productclass import Product


class ProductParser(Spider):
    name = 'orsay-parse'

    def parse(self, response):
        product = Product()

        product['brand'] = 'orsay'
        product['care'] = self.product_care(response)
        product['category'] = self.product_category(response)
        product['discription'] = self.product_discription(response)
        product['image_urls'] = self.product_image_urls(response)
        product['retailer_sku'] = self.product_id(response)
        product['name'] = self.product_name(response)
        product['skus'] = {self.sku_id(response): self.product_sku(response)}
        product['url'] = response.url
        product['request_queue'] = self.product_colors_links(response)

        return self.next_request(product)

    def parse_request(self, response):
        item = response.meta['item']
        item_skus = item['skus']
        item_skus.update(self.product_sku(response))
        item['skus'] = item_skus
        item['image_urls'] += self.product_image_urls(response)

        return self.next_request(item)

    def next_request(self, item):
        color_links = item['request_queue']
        if color_links:
            link = color_links.pop()
            req = scrapy.Request(url=link, callback=self.parse_request)
            req.meta['item'] = item
            yield req
        else:
            item.pop('request_queue')
            yield item

    def product_sku(self, response):
        sku = {}

        sku['color'] = self.product_selected_color(response)
        sku['price'] = self.product_price(response)
        sku['currency'] = self.product_currency(response)
        sku['size'] = self.product_size(response)

        return {self.sku_id: sku}

    def product_care(self, response):
        css = '.product-material p::text'
        return response.css(css).extract()

    def product_category(self, response):
        css = '.breadcrumb a:nth-last-child(2) span::text'
        return response.css(css).extract_first()

    def product_discription(self, response):
        css = '.with-gutter::text'
        return response.css(css).extract()

    def product_image_urls(self, response):
        css = '.productthumbnail::attr(src)'
        return response.css(css).extract()

    def product_name(self, response):
        css = '.product-name::text'
        return response.css(css).extract_first()

    def product_color(self, response):
        colors = []
        css = '.swatches color a::attr(title)'

        for item in response.css().extract(css):
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
        return price.strip()

    def product_size(self, response):
        css = '.size li.selected a::text'
        size = response.css(css).extract_first()

        return size.strip() if size else "One Size"

    def sku_id(self, response):
        css = '.js-product-content-gtm::attr(data-product-details)'
        data = response.css(css).extract_first()
        data = json.loads(data)
        return data['idListRef12']

    def product_colors_links(self, response):
        xpath = '//ul[contains(@class, "swatches color")]/'\
                'li[not(contains(@class, "selected"))]//a/@href'
        return response.xpath(xpath).extract()

    def product_id(self, response):
        css = '.js-product-content-gtm::attr(data-product-details)'
        data = response.css(css).extract_first()
        data = json.loads(data)
        return data['idListRef6']
