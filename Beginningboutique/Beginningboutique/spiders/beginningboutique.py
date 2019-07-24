# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from Beginningboutique.items import BeginningboutiqueItem


class Beginningboutique(CrawlSpider):
    name = "beginningboutique"
    allowed_domains = ['beginningboutique.com.au']
    start_urls = ['https://www.beginningboutique.com.au/']
    market = "AU"
    retailer = 'beginningboutique-au'
    gender = "women"

    rules = (
        Rule(LinkExtractor(
            restrict_css=[".header-nav-wrapper",
                          ".pagination"]),
             callback='parse'),

        Rule(LinkExtractor(
            restrict_css="#shopify-section-collection"),
            callback='product_parse')
    )

    def parse(self, response):
        for request in super(Beginningboutique, self).parse(response):
            trail = response.meta.get('trail', [])
            trail_name = response.css('.section-heading__heading::text').get()
            request.meta['trail'] = trail + [trail_name, [response.url]]
            yield request

    def product_parse(self, response):
        product = BeginningboutiqueItem()
        product = self.boilerplate(product, response)
        product['retailer_sku'] = self.retailer_sku(response)
        product['category'] = self.category(response)
        product['brand'] = self.brand(response)
        product['name'] = self.product_name(response)
        product['description'] = self.description(response)
        product['care'] = self.care(response)
        product['image_urls'] = self.image_urls(response)
        product['skus'] = self.skus(response)
        product['price'] = self.price(response)
        product['currency'] = self.currency(response)
        return product

    def boilerplate(self, product, response):
        product['market'] = self.market
        product['retailer'] = self.retailer
        product['spider_name'] = self.name
        product['gender'] = self.gender
        product['crawl_start_time'] = self.crawler.stats.get_stats()['start_time'].strftime("%Y-%m-%dT%H:%M:%s")
        product['trail'] = response.meta.get('trail')
        product['url'] = response.url
        product['url_original'] = response.url
        product['industry'] = None
        return product

    def product_name(self, response):
        return response.css('.product-heading__title::text').get()

    def retailer_sku(self, response):
        return response.css('.product-heading *::attr(data-product-id)').get()

    def category(self, response):
        return response.css('#shopify-section-related-collections * a::text').getall()

    def brand(self, response):
        return response.css('.product-heading * a::text').get()

    def description(self, response):
        return response.css('span:contains(DESCRIPTION) + .product__specs-detail ::text').getall()

    def care(self, response):
        return response.css('span:contains(FABRICATION) + .product__specs-detail ::text').getall()

    def image_urls(self, response):
        return response.css('.product-images-wrapper * img::attr(src)').getall()

    def skus(self, response):
        skus = {}
        css = 'script:contains("variants")::text'
        raw_color = response.css(css).re_first('"sku":"(.*?)"')
        common_sku = {'colour': raw_color.split('-')[-2]} if raw_color else {}
        common_sku.update({
            'price': self.price(response),
            'currency': self.currency(response)
        })

        for size in response.css('#SingleOptionSelector-0 > option::text').getall():
            sku = common_sku.copy()
            sku['size'] = size
            skus[f'{sku["colour"]}_{size}' if raw_color else size] = sku

        return skus

    def price(self, response):
        return float(response.css('.product__price * span::text').get()[1:])

    def currency(self, response):
        return response.css('.product__price * span::text').get()[0]
