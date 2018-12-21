# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractor import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
import json


class DrmartensSpider(scrapy.Spider):
    name = 'drmartens_au_spider'
    allowed_domains = ['www.drmartens.com.au']
    start_urls = ['http://www.drmartens.com.au/']
    visited_urls = []
    products = {}

    rules = [
        Rule(
            LinkExtractor(
                canonicalize=True,
                unique=True,
            ),
            follow=True
        )
    ]

    def parse(self, response):
        links = LinkExtractor().extract_links(response)

        for link in links:
            if self.is_allowed_link(link):
                yield scrapy.Request(link.url, callback=self.parse_page)

    def parse_page(self, response):
        item = {}
        item['retailer_sku'] = self.get_product_id(response)

        if item['retailer_sku'] and item['retailer_sku'] not in self.products:
            item['name'] = self.get_product_name(response)
            item['care'] = self.get_care_content(response)
            item['url'] = response.url
            item['spider_name'] = 'drmartens_au'
            item['market'] = 'AU'
            item['retailer'] = 'drmartens-au'
            item['brand'] = 'Dr. Martens'
            item['category'] = self.get_product_category(response)
            item['description'] = self.get_product_description(response)
            item['image_urls'] = self.extract_image_urls(response)

            self.visited_urls.append(response.request.headers.get('Referer', None))
            item['trail'] = self.visited_urls

            price_details = self.get_price_details(response)
            if price_details:
                item['price'] = float(price_details[0]) * 100
                item['currency'] = price_details[1]

            self.products[item['retailer_sku']] = item

            yield item
        else:
            links = LinkExtractor().extract_links(response)

            for link in links:
                if self.is_allowed_link(link):
                    yield scrapy.Request(link.url, callback=self.parse_page)

        self.visited_urls = []

    def get_product_id(self, response):
        return response.css('.extra-product::attr(data-sku)').extract_first()

    def get_product_name(self, response):
        return response.css('.product-info-main .page-title span::text').extract_first()

    def get_care_content(self, response):
        care_content = response.css('.additional-attributes .large-4 .content-short-description p::text').extract()
        return [care.strip() for care in care_content if care.strip()]

    def get_price_details(self, response):
        return response.css('.price-final_price meta::attr(content)').extract()

    def get_product_category(self, response):
        category = response.css('.breadcrumbs .item strong::text').extract_first()
        if category:
            return category.strip()

    def get_product_description(self, response):
        description = response.css('.additional-attributes .large-8 .content::text').extract_first()
        if description:
            return [x.strip() for x in description.split('.') if x.strip()]

    def extract_image_urls(self, response):
        image_urls = []
        images_data = response.xpath("//script[contains(., 'mage/gallery/gallery')]/text()").extract_first()
        if images_data:
            images_data = images_data.split('\n')
            images_data = [x.strip().strip(',').strip(' "data": ') for x in images_data if 'data":' in x]
            image_urls = [image['img'] for image in json.loads(images_data[0])]

        return image_urls

    def is_allowed_link(self, link):
        is_allowed = False
        for allowed_domain in self.allowed_domains:
            if allowed_domain in link.url:
                is_allowed = True

        return is_allowed
