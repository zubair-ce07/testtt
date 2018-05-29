# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re


class SchutzSpider(CrawlSpider):
    name = 'schutzspider'
    allowed_domains = ['schutz.com.br']
    start_urls = ['https://schutz.com.br/store/']
    xpaths = ['//div[@class="sch-main-menu-sub-links-left"]',
                 '//ul[@class="pagination"]/li[@class="next"]']

    # Follow any link scrapy finds (that is allowed and matches the patterns).
    rules = [Rule(LinkExtractor(
                restrict_xpaths=xpaths
                ), callback='parse'),
                Rule(LinkExtractor(
                restrict_xpaths='//a[@class="sch-category-products-item-link"]'
                ), callback='parse_product', follow=True)]
 
    def parse(self, response):
        requests = super(SchutzSpider, self).parse(response)
        for request in requests:
            request.meta['trail'] = ['https://schutz.com/br']
            request.meta['trail'].append(response.url)
            yield request

    @staticmethod
    def clean_price_list(price_list):
        cleaned_price_list = []
        for prices in price_list:
            prices = re.findall('\d+', prices)
            if prices:
                cleaned_price_list.append(int(prices[0]) * 100)
        return cleaned_price_list

    @staticmethod
    def description(response):
        description_text = '.sch-description-content p::text'
        description_list = '.sch-description-list li'

        description = [response.css(description_text).extract_first()]
        for list_item in response.css(description_list):
            span_text = list_item.css('span::text').extract_first()
            strong_text = list_item.css('strong::text').extract_first()
            description.append(f"{span_text}: {strong_text}")  
        return description

    @staticmethod
    def color(description):
        for list_item in description[1:]:
            if 'Cor' in list_item:
                return list_item.split(':')[1]
        return None

    @staticmethod
    def care(description):
        care = []
        for list_item in description[1:]:
            if 'Material' in list_item:
                care.append(list_item)
        return care

    @staticmethod
    def prices(response):
        price_list = response.css('.sch-price ::text').extract()
        price_list = set(SchutzSpider.clean_price_list(price_list))
        return sorted(price_list)

    @staticmethod
    def category(response):
        category_list = response.css('.clearfix a::text').extract()
        return category_list[1:-1]

    @staticmethod
    def sku(response):
        color_dictionary = {}
        price = SchutzSpider.prices(response)[0]
        color = SchutzSpider.color(SchutzSpider.description(response))
        drop_down_sel = '.sch-notify-form .sch-form-group-select select option'
        list_sel = '.sch-sizes label'
        sizes = response.css(list_sel) or response.css(drop_down_sel)
        for size in sizes:
            dictionary = {'color': color, 'currencey': 'BRL', 'price': price}
            size_value = size.css(' ::text').extract_first()
            dictionary['size'] = size_value
            if 'sch-avaiable' in size.xpath("@class").extract_first():
                dictionary['out_of_stock'] = False
            else:
                dictionary['out_of_stock'] = True
            color_dictionary[f"{color}{size_value}"] = dictionary
        return color_dictionary

    def is_out_of_stock(sku):
        for key, value in sku.items():
            if not value['out_of_stock']:
                return False
        return True

    def retailer_sku(response):
        retailer_sku_sel = '.sch-pdp::attr(data-product-code)'
        return response.css(retailer_sku_sel).extract_first()

    def name(response):
        name_sel = '.sch-sidebar-product-title::text'
        return response.css(name_sel).extract_first()

    def trail(response):
        trail = response.meta['trail']
        trail.append(response.url)
        return trail

    def parse_product(self, response):
        price = SchutzSpider.prices(response)
        description = SchutzSpider.description(response)
        sku = SchutzSpider.sku(response)

        yield {
            'brand': 'Schutz',
            'care': SchutzSpider.care(description),
            'category': SchutzSpider.category(response),
            'currency': 'BRL',
            'description': description,
            'name': SchutzSpider.name(response),
            'price': price[0],
            'previous-prices': price[1:],
            'retailer_sku': SchutzSpider.retailer_sku(response),
            'sku': sku,
            'trail': SchutzSpider.trail(response),
            'url': response.url,
            'out-of-stock': SchutzSpider.is_out_of_stock(sku),
        }
