# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import requests


class SheegoSpider(scrapy.Spider):
    name = 'sheegocrawler'
    allowed_domains = ['www.sheego.de/']
    start_urls = ['https://www.sheego.de/basic-stretch-bluse-mit-kurzem-arm_115639.html?color=00878']

    # def parse(self, response):
    #     print(response.css('div.header__area.header__area--nav > section > section > div:nth-child(-n+7) > a::attr(href)').extract())
    #     pass

    def parse_main_products(self, response):

        # getting product link on same page
        print(response.css('#page-content > section > div.l-f > div > div.c-pl > '
                           'section.pl__list.js-productList.at-product-list > section > div > div.js-product__wrapper'
                           '> a.js-product__link::attr(href)').extract())

        # getting next page link
        print(response.css('span.paging__btn.paging__btn--next > a::attr(href)').extract())

    def parse(self, response):
        print(self.care(response))
        print(self.description(response))
        print(self.product_name(response))
        # item = {
        #     'care': self.care(response),
        #     'description': self.description(response),
        #     'type': self.product_type(response),
        #     'image_url': self.image_url(response),
        #     'product_name': self.product_name(response),
        #     'sku': self.sku_id(response),
        #     'url': response.url,
        #     #'skus': self.populate_sku_for_all_sizes(response)
        # }
        #
        # yield item
        pass

    def image_url(self, response):
        return response.urljoin(response.css('.product-slider-image > div.item > picture > source::'
                                             'attr(srcset)')[0].extract())
    def product_name(self, response):
        return response.css('div.l-f.l-f-w-w.l-f-a-c.at-dv-title-box > h1::text').extract()[0].strip()

    def product_type(self, response):
        return response.css('.breadcrumb > ul:nth-child(1) > li:nth-child(3) > a:nth-child(1)::'
                            'text').extract()[0].strip()

    def care(self, response):
        return ', '.join(t.strip() for t in response.css('.p-details__material.l-mb-10.l-mb-20-md.l-mb-0-md > tbody > tr > td:nth-child(2)::text').extract())

    def description(self, response):
        return ', '.join(t.strip() for t in response.css('div.l-hidden-xs-s.l-startext > div >'
                            ' ul > li::text').extract()).strip()

    def sku_id(self, response):
        return response.css('div.mobile_toggle:nth-child(1) > p:nth-child(1)::text').extract()[0].split(':')[1]