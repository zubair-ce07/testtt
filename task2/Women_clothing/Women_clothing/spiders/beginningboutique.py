# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from Women_clothing.items import BeginningboutiqueItem


class MySpider(CrawlSpider):
    name = "beginningboutique"
    allowed_domains = ['beginningboutique.com.au']
    start_urls = ['https://www.beginningboutique.com.au/']

    rules = (
        Rule(LinkExtractor(
            allow=('beginningboutique.com.au', ),
            restrict_xpaths=("//div[@class='header-nav-wrapper']"))),

        Rule(LinkExtractor(
            allow=('beginningboutique.com.au/products', ),
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
            crawl_start_time=self.start_time()
        )

    def product_name(self, response):
        return response.css('.product-heading__title::text').extract_first()

    def retailer_sku(self, response):
        return response.xpath(
            "//div[@class='product__heart']/div/@data-product-id").get()

    def trail(self, response):
        return response.request.headers.get('referer', None)

    def category(self, response):
        return response.xpath(
            "//div[@id='shopify-section-related-collections']/"
            "/a[@href]/text()").getall()

    def brand(self, response):
        return response.xpath(
            '//div[@class="product-heading"]//a/text()').get()

    def url(self, response):
        return response.request.url

    def description(self, response):
        product_details = response.xpath(
            "//div[@class='product__specs']//li[1]//p/text()").getall()
        if not product_details:
            product_details = response.xpath(
                "//div[@class='product__specs']//li[1]/"
                "div/text()").getall()
            detail_reference = response.xpath(
                "//div[@class='product__specs-detail']"
                "/a[@href]/text()").getall()
            for j in range(len(product_details), -1, -1):
                if len(detail_reference) > j:
                    product_details.insert(j + 1, detail_reference[j])

        detail_list = response.xpath(
            '//div[@class="product__specs-detail"]/'
            'ul/li/text()').getall()
        return product_details + detail_list

    def care(self, response):
        care = response.xpath(
            "//ul[@class='product__specs-list']/li[2]//li/text()").getall()
        if not care:
            care = response.xpath(
                "//div[@class='product__specs']//div/text()").getall()
        return care

    def image_urls(self, response):
        return response.xpath(
            "//div[@class='product-images-wrapper']//img/@src").getall()

    def skus(self, response):
        meta = response.xpath(
            "//head/script[contains"
            "(., 'window.ShopifyAnalytics.meta.currency')]"
            "/text()").getall()
        script_data = meta[0].split(';\n')
        meta_data = ''
        for i in script_data:
            if i[:8] == 'var meta':
                meta_data = i[22:-1]
        string_meta = str(meta_data)
        start = 0
        end = 0
        for i in range(len(string_meta)):
            if string_meta[i:i + 8] == 'variants':
                start = i + 10
            if string_meta[i:i + 3] == '}]}':
                end = i + 2
        skus = string_meta[start:end]
        return skus

    def price(self, response):
        return response.css('.money::text').extract_first()

    def currency(self, response):
        if self.price(response)[0] == "$":
            return "AUD"
        else:
            return self.price(response)[0]

    def start_time(self):
        return self.crawler.stats.get_stats()['start_time']
