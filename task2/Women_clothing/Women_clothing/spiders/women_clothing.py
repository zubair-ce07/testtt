# -*- coding: utf-8 -*-
import scrapy


class QuotesSpiderSpider(scrapy.Spider):

    name = "women_clothing"
    web_details = []
    allowed_domains = ['beginningboutique.com.au']

    def start_requests(self):
        urls = [
            'https://www.beginningboutique.com.au/collections/new',
            'https://www.beginningboutique.com.au/collections/dresses',
            'https://www.beginningboutique.com.au/collections/festival-outfits',
            'https://www.beginningboutique.com.au/collections/all',
            'https://www.beginningboutique.com.au/collections/accessories',
            'https://www.beginningboutique.com.au/collections/womens-shoes',
            'https://www.beginningboutique.com.au/collections/brands',
            'https://www.beginningboutique.com.au/collections/sale',
        ]
        for url in urls:
            yield scrapy.Request(url=url,
                                 callback=self.parse)

    def parse(self, response):
        print("url:   ", response.request.url)
        collections = response.xpath("//div[@id='shopify-section-collection']/"
                                     "div/div/div/div/div/a[contains(@href, '')]/@href").getall()
        for product_url in collections:
            yield scrapy.Request(url=('https://www.beginningboutique.com.au' + product_url),
                                 callback=self.product_parse,
                                 dont_filter=True)

    def product_parse(self, response):
        page_deatils = {
            'retailer_sku': self.retailer_sku(response),
            'gender': "women",
            'trail': self.trail(response),
            'category': self.related_items(response),
            'industry': 'null',
            'brand': self.retailer(response),
            'url': self.url(response),
            'market': self.market(response),
            'retailer_url': self.retailer_url(response),
            'url_original': self.url(response),
            'product_name': self.product_name(response),
            'description': self.product_details(response),
            'care': self.fabric(response),
            'image_urls': self.image_url(response),
            'skus': self.skus(response),
            'price': self.money(response),
            'currence': self.currency(response),
            'spider_name': 'women_clothing',
            'crawl_start_time': self.start_time()
        }
        return page_deatils

    @staticmethod
    def product_name(response):
        return response.css('.product-heading__title::text').extract_first()

    @staticmethod
    def retailer_sku(response):
        return response.xpath(
            "//div[@class='product__heart']/div/@data-product-id").get()

    @staticmethod
    def trail(response):
        return response.request.headers.get('referer', None)

    @staticmethod
    def related_items(response):
        return response.xpath(
            "//div[@id='shopify-section-related-collections']/"
            "div/div/div/p/a[contains(@href, '')]/text()").getall()

    @staticmethod
    def retailer(response):
        return response.xpath('//div[@class="product-heading"]/p/a/text()').getall()

    @staticmethod
    def url(response):
        return response.request.url

    @staticmethod
    def market(response):
        url = response.request.url
        domain = url.split('/')[2]
        url_len = len(domain) - 1
        while domain[url_len] != ".":
            url_len -= 1
        market = domain[url_len + 1:]
        return market

    @staticmethod
    def retailer_url(response):
        return response.xpath('//div[@class="product-heading"]/p/a/@href').getall()

    @staticmethod
    def product_details(response):
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

    @staticmethod
    def fabric(response):
        fabric = response.xpath(
            "//div[@class='product__specs']/ul[@class='product__specs-list']/"
            "li[2]/div[@class='product__specs-detail']/ul/div/li/text()").getall()
        if len(fabric) == 0:
            fabric = response.xpath(
                "//div[@class='product__specs']/ul[@class='product__specs-list']/"
                "li[2]/div[@class='product__specs-detail']/text()").getall()
        return fabric

    @staticmethod
    def image_url(response):
        return response.xpath("//div[@class='product-images-wrapper']/div/div/img/@src").getall()

    @staticmethod
    def skus(response):
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

    @staticmethod
    def money(response):
        return response.css('.money::text').extract_first()

    def currency(self, response):
        return self.money(response)[0]

    def start_time(self):
        return self.crawler.stats.get_stats()['start_time']
