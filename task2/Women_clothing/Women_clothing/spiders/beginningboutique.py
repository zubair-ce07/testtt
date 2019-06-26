# -*- coding: utf-8 -*-
import scrapy
from WebData import WebData


class Beginningboutique(scrapy.Spider):

    name = "beginningboutique"
    web_details = []
    allowed_domains = ['beginningboutique.com.au']

    def start_requests(self):
        start_url = 'https://www.beginningboutique.com.au'
        yield scrapy.Request(url=start_url,
                             callback=self.parse)

    def parse(self, response):
        categories = response.xpath("//div[@class='header-nav-wrapper']/"
                                    "/div[@class='dropdown-wrapper']/a[contains(@href, '')]/@href").getall()
        for url in categories:
            yield scrapy.Request(url=('https://www.beginningboutique.com.au'+url),
                                 callback=self.parse_products_urls, dont_filter=True)

    def parse_products_urls(self, response):
        product_urls = response.xpath("//div[@id='shopify-section-collection']/"
                                      "/a[contains(@href, '')]/@href").getall()
        for product_url in product_urls:
            yield scrapy.Request(url=('https://www.beginningboutique.com.au' + product_url),
                                 callback=self.product_parse,
                                 dont_filter=True)

    def product_parse(self, response):
        page_deatils = WebData(
            retailer_sku=self.retailer_sku(response),
            trail=self.trail(response),
            category=self.category(response),
            brand=self.brand(response),
            url=self.url(response),
            retailer=self.retailer(response),
            url_original=self.url(response),
            product_name=self.product_name(response),
            description=self.description(response),
            care=self.care(response),
            image_url=self.image_url(response),
            skus=self.skus(response),
            price=self.price(response),
            currence=self.currency(response),
            spider_name='beginningboutique',
            crawl_start_time=self.start_time()
        )
        return page_deatils

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
            "div/div/div/p/a[contains(@href, '')]/text()").getall()

    def brand(self, response):
        return response.xpath('//div[@class="product-heading"]/p/a/text()').get()

    def url(self, response):
        return response.request.url

    def retailer(self, response):
        return response.xpath('//div[@class="product-heading"]/p/a/@href').getall()

    def description(self, response):
        product_details = response.xpath(
            "//div[@class='product__specs']/ul[@class='product__specs-list']/"
            "li[1]/div[@class='product__specs-detail']/p/text()").getall()
        if len(product_details) == 0:
            product_details = response.xpath(""
                                             "//div[@class='product__specs']/ul[@class='product__specs-list']/"
                                             "li[1]/div[@class='product__specs-detail']/text()").getall()
            detail_reference = response.xpath(
                "//div[@class='product__specs-detail']/a[contains(@href, '')]/text()").getall()
            for j in range(len(product_details), -1, -1):
                if len(detail_reference) > j:
                    product_details.insert(j + 1, detail_reference[j])

        detail_list = response.xpath('//div[@class="product__specs-detail"]/ul/li/text()').getall()
        return product_details + detail_list

    def care(self, response):
        fabric = response.xpath(
            "//div[@class='product__specs']/ul[@class='product__specs-list']/"
            "li[2]/div[@class='product__specs-detail']/ul/div/li/text()").getall()
        if len(fabric) == 0:
            fabric = response.xpath(
                "//div[@class='product__specs']/ul[@class='product__specs-list']/"
                "li[2]/div[@class='product__specs-detail']/text()").getall()
        return fabric

    def image_url(self, response):
        return response.xpath("//div[@class='product-images-wrapper']/div/div/img/@src").getall()

    def skus(self, response):
        meta = response.xpath("//head/script[contains(., 'window.ShopifyAnalytics.meta.currency')]/text()").getall()
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
