#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from witt_weiden.items import WittWeidenItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http.request import Request
import re


class WittWeidenSpider(CrawlSpider):
    name = "WittWeidenSpider"
    allowed_domains = ["witt-weiden.de"]
    start_urls = [
        "http://www.witt-weiden.de/"
    ]
    main_menu_xpath = './/*[@id="nav-products"]/ul/li/a'    # xpath for main menu
    sub_menu_xpath = './/*[@class="nav subnav-list"]//a'    # xpath for sub menu
    products_page_xpath = './/*[@id="article-grid"]//a'     # xpath for product
    pagination_xpath = './/*[@id="content-footer"]//a[contains(descendant::span,"Weiter")]'
    rules = [

        Rule(LinkExtractor(restrict_xpaths=main_menu_xpath)),
        Rule(LinkExtractor(restrict_xpaths=sub_menu_xpath)),
        Rule(LinkExtractor(restrict_xpaths=products_page_xpath),
             callback='get_product_detail'),
        Rule(LinkExtractor(restrict_xpaths=pagination_xpath))
    ]

    def get_product_detail(self, response):
        item = WittWeidenItem()
        item['retailer'] = 'witt-weiden'
        item['spider_name'] = self.name
        item['category'] = self.get_cat(response)
        item['url'] = response.url
        item['care'] = self.get_care(response)
        item['title'] = self.get_title(response)
        item['description'] = self.get_description(response)
        item['image_urls'] = []
        colors = []
        size_with_price = {}
        if response.xpath(".//*[@id='color-control-group']"):
            colors = response.xpath(
                ".//*[@id='color-control-group']/div/ul/li/a[not(contains(@href,'#'))]/@href"). \
                extract()
            return self.request_for_color(colors, item, size_with_price)
        else:  # execute when color drop down not present
            self.get_images(response, item)
            if response.xpath(".//*[@id='model-control-group']"):  # check models are available
                models = response.xpath(
                    ".//*[@id='model-control-group']//ul//li/a[not(contains(@href,'#'))]/@href"). \
                    extract()
                return self.request_for_models(models, colors, item, size_with_price)
            else:
                if response.xpath(".//*[@id='size-control-group']"): # check sizes are available
                    sizes = response.xpath(
                        ".//*[@id='size-control-group']//ul/li/a[not(contains(@href,'#'))]/@href"). \
                        extract()
                    return self.request_for_size(sizes, colors, item, size_with_price, None)
                else:
                    price = self.get_price(response)
                    color = self.get_color(response)
                    size = self.get_size(response)
                    size_with_price[size + "_" + color] = {'color': color,
                                                           'size': size,
                                                           'price': price}
                    item['skus'] = self.get_skus(size_with_price)
                    return item

    def request_for_size(self, sizes, colors, item, size_with_price, models):
        return Request(url=sizes.pop(0), callback=self.parse_price_from_sizes,
                       meta={'color': colors,
                             'item': item,
                             'sizes': sizes,
                             'size_with_price': size_with_price, 'models': models})

    def request_for_color(self, colors, item, size_with_price):
        return Request(url=colors.pop(0), callback=self.parse_colors_from_product,
                       meta={'color': colors,
                             'item': item,
                             'size_with_price': size_with_price})

    def request_for_models(self, models, colors, item, size_with_price):
        return Request(url=models.pop(0), callback=self.parse_size_from_models,
                       meta={'color': colors,
                             'item': item,
                             'models': models,
                             'size_with_price': size_with_price}, dont_filter=True)

    def parse_size_from_models(self, response):  # get sizes from models
        size_with_price = response.meta['size_with_price']
        colors = response.meta['color']
        item = response.meta['item']
        models = response.meta['models']
        if response.xpath(".//*[@id='size-control-group']"):
            sizes = response.xpath(
                ".//*[@id='size-control-group']//ul/li/a[not(contains(@href,'#'))]/@href"). \
                extract()
            return self.request_for_size(sizes, colors, item, size_with_price, models)

        else:
            price = self.get_price(response)
            color = self.get_color(response)
            size = self.get_size(response)
            size_with_price[size + "_" + color] = {'color': color,
                                                   'size': size,
                                                   'price': price}
        if models:
            if colors:
                return self.request_for_color(colors, item, size_with_price)
            else:
                item['skus'] = self.get_skus(size_with_price)
                return item

    def parse_price_from_sizes(self, response):  # get price from sizes
        size_with_price = response.meta['size_with_price']
        colors = response.meta['color']
        sizes = response.meta['sizes']
        models = response.meta['models']
        item = response.meta['item']
        size = self.get_size(response)
        price = self.get_price(response)
        color = self.get_color(response)
        size_with_price[size + "_" + color] = {'color': color,
                                               'size': size,
                                               'price': price}
        if sizes:
            return self.request_for_size(sizes, colors, item, size_with_price, models)
        elif models:
            return self.request_for_models(models, colors, item, size_with_price)
        elif colors:
            return self.request_for_color(colors, item, size_with_price)
        else:
            item['skus'] = self.get_skus(size_with_price)
            return item

    def parse_colors_from_product(self, response):  # parse colors/ sizes / models  from product
        colors = response.meta['color']
        item = response.meta['item']
        size_with_price = response.meta['size_with_price']
        self.get_images(response, item)
        if response.xpath(".//*[@id='model-control-group']"):
            models = response.xpath(
                ".//*[@id='model-control-group']//ul//li/a[not(contains(@href,'#'))]/@href"). \
                extract()
            return self.request_for_models(models, colors, item, size_with_price)
        else:
            if response.xpath(".//*[@id='size-control-group']"):
                sizes = response.xpath(
                    ".//*[@id='size-control-group']//ul/li/a[not(contains(@href,'#'))]/@href"). \
                    extract()
                return self.request_for_size(sizes, colors, item, size_with_price, None)
            else:
                price = self.get_price(response)
                color = self.get_color(response)
                size = self.get_size(response)
                size_with_price[size + "_" + color] = {'color': color,
                                                       'size': size,
                                                       'price': price}
                if colors:
                    return self.request_for_color(colors, item, size_with_price)
                else:
                    item['skus'] = self.get_skus(size_with_price)
                    return item

    def get_images(self, response, item):
        images = response.xpath('.//*[@id="backviews" or @id="desktopZoom"]//img/@src').extract()
        for img in images:
            img = 'http://www.witt-weiden.de' + img
            img = img.replace('_4.jpg', '_5.jpg')
            item['image_urls'].append(img)

    def get_title(self, response):
        title = response.xpath('.//*[@id="article-header"]/header/h1/text()') \
            .extract()[0]
        return title.strip()

    def get_care(self, response):
        care = response.xpath('.//tr[contains(descendant::th,"Pflege")]/td/text()') \
            .extract()
        return care

    def get_size(self, response):
        if response.xpath(".//*[@id='size-control-group']"):
            size = response.xpath(".//*[@id='size-control-group']//button/text()") \
                .extract()[0]
        elif response.xpath('.//tr[contains(descendant::th,"Größen")]'):
            size = response.xpath('.//tr[contains(descendant::th,"Größen")]/td/text()') \
                .extract()[0]
        else:
            size = 'OneSize'

        return size.strip()

    def get_cat(self, response):
        categoryResponse = response.xpath('.//script[contains(.,"emospro.pageId")]/text()') \
            .extract()[0]
        match = re.search(r"pageId = 'Angebotsstrecke/Artikeldetailseite/*(.*)'", categoryResponse)
        category_raw_value = match.group(1)
        categories = [category for category in category_raw_value.split('/') if category.strip()]
        return categories

    def get_color(self, response):
        if response.xpath(".//*[@id='color-control-group']"):
            color = response.xpath(".//*[@id='color-control-group']//button/text()") \
                .extract()[0]
        else:
            color = response.xpath('.//tr[contains(descendant::th,"Farben")]/td/text()') \
                .extract()[0]
        return color.strip()

    def get_description(self, response):
        description = response.xpath('.//*[@id="description-text"]/p/text()') \
            .extract()
        return description

    def get_price(self, response):
        new_price = response.xpath('.//*[@id="article-price"]//strong/text()') \
            .extract()[0].strip()
        old_price = response.xpath('.//*[@id="article-price"]//strike/text()') \
            .extract()
        currency_symbol = response.xpath('.//*[@id="article-price"]//*[@class="currency-symbol"]/text()') \
            .extract()[0].strip()
        price_in_points = response.xpath('.//*[@id="article-price"]//strong/sup/text()') \
            .extract()[0].strip()
        if len(old_price) == 0:
            return (' ').join(new_price.split()) + price_in_points + currency_symbol
        else:
            return {'new_price': ' '.join(new_price.split()) + price_in_points + currency_symbol,
                    'old_price': ' '.join(old_price[0].split()) + currency_symbol}

    def get_skus(self, size):
        skus = size
        return skus
