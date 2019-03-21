# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import datetime


class FashionSpider(scrapy.spiders.CrawlSpider):
    name = 'fashion_spider'
    start_urls = ['https://www.selectfashion.co.uk/']
    category_css = ['.dropdown-menu-link']
    product_css = ['.catproduct']

    rules = (
        Rule(LinkExtractor(restrict_css=category_css)),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')
    )

    def parse_item(self, response):
        yield {
            'ppid': self.product_id(response),
            'gender': 'women',
            'category': self.product_category(response),
            'url': self.current_page_url(response),
            'date': self.current_date(response),
            'price': self.product_price(response),
            'name': self.product_name(response),
            'description': self.product_description(response),
            'care': self.product_care(response),
            'image_url': self.image_url(response),
            'skus': self.parse_product_detail(response),
        }

    def product_id(self, response):
        return response.css('input[name = "product_id[]"]::attr(value)').get()

    def product_name(self, response):
        return response.css('h1.product-title.uppercase::text').get(),

    def product_description(self, response):
        return response.css('div.panel-body::text').get().strip().split('.')[0]

    def product_care(self, response):
        return response.css('div.panel-body::text').get().strip().split('.')[1:]

    def product_price(self, response):
        return response.css('meta[itemprop="price"]::attr(content)').get()

    def product_category(self, response):
        return response.css('ul.breadcrumb > li > a::text').getall()

    def image_url(self, response):
        return response.css('a.zoom ::attr(src)').getall()

    def current_page_url(self, response):
        return response.css('link[rel = "canonical"]::attr(href)').get()

    def current_date(self, response):
        now = datetime.datetime.now()
        return str(now)

    def parse_product_detail(self, response):
        product_detail = []

        price = self.product_price(response)
        currency = response.css('meta[itemprop="priceCurrency"]::attr(content)').get()
        size_options = response.css('div.attribute_size > select > option[style="font-weight: bold"]::text').getall()
        url = self.current_page_url(response)
        colour = url.split('_')[1].split('.')[0]

        for sku_id in size_options:
            size = sku_id.split('-')
            if len(size) > 1 and size[1] == ' SOLD OUT':
                product_detail.append(f"price: {price} currency: {currency} colour: {colour} out_of_stock = true "
                                      f"size: {size[0]}  sku_id: {colour}_{size[0]}")
            else:
                product_detail.append(f"price: {price} currency: {currency} colour: {colour} size: {size[0]}"
                                      f"sku_id: {colour}_{sku_id}")

        return product_detail
