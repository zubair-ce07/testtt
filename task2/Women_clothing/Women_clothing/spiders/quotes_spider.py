# -*- coding: utf-8 -*-
import scrapy
import json


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
        product = response.css('.product-heading__title::text').extract_first()
        money = response.css('.money::text').extract_first()
        product_details = response.xpath(
            "//div[@class='product__specs']/ul[@class='product__specs-list']/"
            "li[1]/div[@class='product__specs-detail']/p/text()").getall()
        if len(product_details) == 0:
            product_details = response.xpath(""
                                             "//div[@class='product__specs']/ul[@class='product__specs-list']/"
                                             "li[1]/div[@class='product__specs-detail']/text()").getall()
        detail_list = response.xpath('//div[@class="product__specs-detail"]/ul/li/text()').getall()
        retailer = response.xpath('//div[@class="product-heading"]/p/a/text()').getall()
        retailer_url = response.xpath('//div[@class="product-heading"]/p/a/@href').getall()
        detail_reference = response.xpath(
            "//div[@class='product__specs-detail']/a[contains(@href, '')]/text()").getall()
        for j in range(len(product_details), -1, -1):
            if len(detail_reference) > j:
                product_details.insert(j + 1, detail_reference[j])
        fabric = response.xpath(
            "//div[@class='product__specs']/ul[@class='product__specs-list']/"
            "li[2]/div[@class='product__specs-detail']/ul/div/li/text()").getall()
        if len(fabric) == 0:
            fabric = response.xpath(
                "//div[@class='product__specs']/ul[@class='product__specs-list']/"
                "li[2]/div[@class='product__specs-detail']/text()").getall()

        measurements = response.xpath(
            "//div[@class='product__specs']/ul[@class='product__specs-list']/"
            "li[3]/div[@class='product__specs-detail']/ul/div/li/text()").getall()
        if len(measurements) == 0:
            measurements = response.xpath(
                "//div[@class='product__specs']/ul[@class='product__specs-list']/"
                "li[3]/div[@class='product__specs-detail']/text()").getall()
        image_url = response.xpath("//div[@class='product-images-wrapper']/div/div/img/@src").getall()
        url = response.request.url
        size = response.xpath(
            "//div[@class='marketing-select-wrapper']/select[@id='SingleOptionSelector-0']/option/text()").getall()
        currency = money[0]
        related_items = response.xpath(
            "//div[@id='shopify-section-related-collections']/"
            "div/div/div/p/a[contains(@href, '')]/text()").getall()

        page_deatils = {
            'productName': product,
            'price': money,
            'productDetail': product_details,
            'detail_list': detail_list,
            'retailer': retailer,
            'fabric': fabric,
            'measurements': measurements,
            'image': image_url,
            'url': url,
            'size': size,
            'currence': currency,
            'related_items': related_items,
            'retailer_url': retailer_url
        }

        self.web_details.append(page_deatils)
        with open('websiteData.json', 'w') as file:
            json.dump(self.web_details, file)


with open('websiteData.json') as json_file:
    data = json.load(json_file)
    for i in range(len(data)):
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ ", data[i]['productName'])
    print(data[0])
