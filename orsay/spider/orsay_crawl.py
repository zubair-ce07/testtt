# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import OrsayProduct


class OrsaySpider(CrawlSpider):
    name = 'orsay_crawl'
    allowed_domains = ['orsay.com']
    start_urls = ['http://orsay.com/']

    rules = (
        Rule(LinkExtractor(restrict_css=['ul#nav', 'a.next'])),
        Rule(LinkExtractor(restrict_css='a.product-image',), callback='parse_products',),
    )

    def parse_products(self, response):
        product = OrsayProduct()
        product['lang'] = self.get_lang(response)
        product['price'] = self.get_price(response)
        product['currency'] = self.get_currency(response)

        product['retailer_sku'] = self.get_retailer_sku(response)
        product['name'] = self.get_name(response)
        product['description'] = self.get_description(response)
        product['img_urls'] = self.get_img_urls(response)

        product['material'] = self.get_material(response)
        product['care'] = self.get_care(response)
        product['category'] = self.get_categories(response)

        product['skus'] = self.get_skus(response)
        colour_urls = self.get_colour_urls(response)
        colour_urls.remove('#')
        if colour_urls:
            request = self.parse_colour_request(colour_urls, product)
            yield request
        else:
            yield product

    def parse_colour_request(self, colour_urls, product):
        request = scrapy.Request(url=colour_urls[0], callback=self.parse_colours)
        request.meta['item'] = product
        request.meta['colour_urls'] = colour_urls
        return request

    def parse_colours(self, response):
        if response.meta:
            product = response.meta['item']
            colour_urls = response.meta['colour_urls']
            colour_urls.pop(0)

            product['img_urls'].append(self.get_img_urls(response))
            product['skus'].update(self.get_skus(response))
            if colour_urls:
                request = self.parse_colour_request(colour_urls, product)
                yield request
            else:
                yield product

    def get_skus(self, response):
        product_id = self.get_product_id(response)
        price = self.get_price(response)
        currency = self.get_currency(response)
        colour = self.get_colour(response)
        current_skus = {}
        sizes_selector = self.get_sizes_selector(response)

        for size_selector in sizes_selector:
            current_size = self.get_size(size_selector)
            quantity = self.get_quantity(size_selector)
            sku_value = {
                'currency': currency,
                'price': price,
                'size': current_size,
                'colour': colour,
                'out_of_stock': False if int(quantity) else True
            }
            sku_key = product_id + '_' + current_size
            current_skus[sku_key] = sku_value
        return current_skus

    def get_sizes_selector(self, response):
        return response.css('div.sizebox-wrapper li.size-box')

    def get_product_id(self, response):
        return response.css('input[name="sku"]::attr(value)').extract_first()

    def get_colour(self, response):
        return response.css('div.no-display > input[name="colour"]::attr(value)').extract_first()

    def get_quantity(self, response):
        return response.css('::attr(data-qty)').extract_first()

    def get_size(self, response):
        return response.css('::text').extract_first().strip()

    def get_categories(self, response):
        return response.css(
            'div.no-display > input[name="category_name"]::attr(value)').extract_first()

    def get_care(self, response):
        return response.css('ul.caresymbols > li > img::attr(src)').extract()

    def get_material(self, response):
        return response.css('p.material::text').extract_first()

    def get_img_urls(self, response):
        return response.css('div.product-image-gallery-thumbs > a::attr(href)').extract()

    def get_description(self, response):
        return response.css('p.description::text').extract_first().strip()

    def get_name(self, response):
        return response.css('h1.product-name::text').extract_first()

    def get_retailer_sku(self, response):
        return self.get_product_id(response)[0:6]

    def get_currency(self, response):
        return response.css('div.sizebox-wrapper::attr(data-currency)').extract_first()

    def get_price(self, response):
        return response.css('span.price::text').extract_first().strip()

    def get_lang(self, response):
        return response.css('html::attr(lang)').extract_first()

    def get_colour_urls(self, response):
        return response.css('ul.product-colour_urls > li a::attr(href)').extract()

