# -*- coding: utf-8 -*-
import scrapy
import re
import json
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from Women_clothing.items import BeginningboutiqueItem


class Beginningboutique(CrawlSpider):
    name = "beginningboutique"
    allowed_domains = ['beginningboutique.com.au']
    start_urls = ['https://www.beginningboutique.com.au/']
    market = "AU"
    retailer = 'beginningboutique-au'
    gender = "women"

    rules = (
        Rule(LinkExtractor(
            deny='/products',
            restrict_xpaths=["//div[@class='header-nav-wrapper']",
                             "//ul[@class='pagination']"]),
             callback='parse'),

        Rule(LinkExtractor(
            allow='/products',
            restrict_xpaths="//div[@id='shopify-section-collection']"),
            callback='product_parse')
    )

    def parse(self, response):
        for request in super(Beginningboutique, self).parse(response):
            trail = response.meta.get('trail') if response.meta.get('trail') else []
            request.meta['trail'] = trail + [response.request.url]
            yield request

    def product_parse(self, response):
        product = BeginningboutiqueItem()
        product = self.boilerplate(product)
        product['retailer_sku'] = self.retailer_sku(response)
        product['trail'] = self.trail(response)
        product['category'] = self.category(response)
        product['brand'] = self.brand(response)
        product['url'] = self.url(response)
        product['url_original'] = self.url(response)
        product['product_name'] = self.product_name(response)
        product['description'] = self.description(response)
        product['care'] = self.care(response)
        product['image_urls'] = self.image_urls(response)
        product['skus'] = self.skus(response)
        product['price'] = self.price(response)
        product['currency'] = self.currency(response)
        return product

    def boilerplate(self, product):
        product['market'] = self.market
        product['retailer'] = self.retailer
        product['spider_name'] = self.name
        product['gender'] = self.gender
        product['crawl_start_time'] = self.crawler.stats.get_stats()['start_time'].strftime("%Y-%m-%dT%H:%M:%s")
        return product

    def product_name(self, response):
        return response.css('.product-heading__title::text').get()

    def retailer_sku(self, response):
        return response.xpath("//div[@class='product__heart']/div/@data-product-id").get()

    def trail(self, response):
        return response.meta.get('trail')

    def category(self, response):
        return response.xpath("//div[@id='shopify-section-related-collections']//a[@href]/text()").getall()

    def brand(self, response):
        return response.xpath('//div[@class="product-heading"]//a/text()').get()

    def url(self, response):
        return response.url

    def description(self, response):
        product_details = response.xpath("//div[@class='product__specs']//li[1]//p/text()").getall()
        if not product_details:
            product_details = response.xpath("//div[@class='product__specs']//li[1]/div/text()").getall()
            detail_reference = response.xpath("//div[@class='product__specs-detail']/a[@href]/text()").getall()
            for details in range(len(product_details), -1, -1):
                if len(detail_reference) > details:
                    product_details.insert(details + 1, detail_reference[details])
        return product_details+response.xpath('//div[@class="product__specs-detail"]/ul/li/text()').getall()

    def care(self, response):
        care = response.xpath("//ul[@class='product__specs-list']/li[2]//li/text()").getall()
        return care or response.xpath("//div[@class='product__specs']//div/text()").getall()

    def image_urls(self, response):
        return response.xpath("//div[@class='product-images-wrapper']//img/@src").getall()

    def skus(self, response):
        path = "//head/script[contains(., 'window.ShopifyAnalytics.meta.currency')]/text()"
        meta = response.xpath(path).get()
        meta_json = json.loads(re.findall(r'"variants.*"}]', meta)[0][11:])
        for variants in meta_json:
            variants.pop('name')
            variants.pop('id')
            sku_in_meta = variants.pop('sku')
            variants['color'] = re.findall(r'-[A-Z|a-z]+', sku_in_meta)
            variants['color'] = variants['color'][0][1:] if variants['color'] else None
            variants['size'] = variants.pop('public_title')
            variants['currency'] = self.currency(response)
        return meta_json

    def price(self, response):
        try:
            return float(response.css('.money::text').get()[1:])
        except:
            return response.css('.money::text').get()[1:]

    def currency(self, response):
        return response.css('.money::text').get()[0]
