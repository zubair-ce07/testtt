# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from Women_clothing.items import BeginningboutiqueItem


class Beginningboutique(CrawlSpider):
    name = "beginningboutique"
    allowed_domains = ['beginningboutique.com.au']
    start_urls = ['https://www.beginningboutique.com.au/']

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths="//div[@class='header-nav-wrapper']")),

        Rule(LinkExtractor(
            allow='/products',
            restrict_xpaths="//div[@id='shopify-section-collection']"),
            callback='product_parse'),
    )

    def product_parse(self, response):
        return BeginningboutiqueItem(
            retailer_sku=self.retailer_sku(response),
            trail=self.trail(response),
            category=self.category(response),
            brand=self.brand(response),
            url=self.url(response),
            url_original=self.url(response),
            product_name=self.product_name(response),
            description=self.description(response),
            care=self.care(response),
            image_urls=self.image_urls(response),
            skus=self.skus(response),
            price=self.price(response),
            currency=self.currency(response),
            crawl_start_time=self.start_time(),
            market="AU",
            retailer='beginningboutique-au',
            spider_name='beginningboutique',
            gender="women"
        )

    def product_name(self, response):
        return response.css('.product-heading__title::text').get()

    def retailer_sku(self, response):
        return response.xpath("//div[@class='product__heart']/div/@data-product-id").get()

    def trail(self, response):
        return response.request.headers.get('referer', None)

    def category(self, response):
        return response.xpath("//div[@id='shopify-section-related-collections']//a[@href]/text()").getall()

    def brand(self, response):
        return response.xpath('//div[@class="product-heading"]//a/text()').get()

    def url(self, response):
        return response.request.url

    def description(self, response):
        product_details = response.xpath("//div[@class='product__specs']//li[1]//p/text()").getall()
        if not product_details:
            product_details = response.xpath("//div[@class='product__specs']//li[1]/div/text()").getall()
            detail_reference = response.xpath("//div[@class='product__specs-detail']/a[@href]/text()").getall()
            for details in range(len(product_details), -1, -1):
                if len(detail_reference) > details:
                    product_details.insert(details + 1, detail_reference[details])

        detail_list = response.xpath('//div[@class="product__specs-detail"]/ul/li/text()').getall()
        return product_details + detail_list

    def care(self, response):
        care = response.xpath("//ul[@class='product__specs-list']/li[2]//li/text()").getall()
        if not care:
            care = response.xpath("//div[@class='product__specs']//div/text()").getall()
        return care

    def image_urls(self, response):
        return response.xpath("//div[@class='product-images-wrapper']//img/@src").getall()

    def skus(self, response):
        path = "//head/script[contains(., 'window.ShopifyAnalytics.meta.currency')]/text()"
        meta = response.xpath(path).get()
        return re.findall(r'"variants.*"}]', meta)[0][11:]

    def price(self, response):
        return response.css('.money::text').get()

    def currency(self, response):
        return self.price(response)[0]

    def start_time(self):
        return self.crawler.stats.get_stats()['start_time']
