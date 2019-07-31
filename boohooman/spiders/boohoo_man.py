# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy_splash import SplashRequest

from ..items import Item, ProductSkus


class BoohooManSpider(scrapy.Spider):
    name = 'boohoo_man'
    allowed_domains = ['www.boohooman.com']
    start_urls = ['https://www.boohooman.com/']
    items_data = {}

    def parse(self, response):
        clothing = response.xpath(
            "//li['@class=has-submenu js-has-submenu js-prevent-event \
            js-menu-tab' and ./a[contains(.,'CLOTHING')]]")
        heading_urls = clothing.css(
            '.menu-vertical.js-menu-vertical > li > a::attr(href)').getall()
        for url in heading_urls:
            yield scrapy.Request(url, callback=self.parse_pages)

    def parse_pages(self, response):
        yield scrapy.Request(
            response.url, callback=self.parse_items, dont_filter=True)
        # pages_url = response.css(
        #     '.pagination-item.device-paginate.js-device-paginate > \
        #     a::attr(href)').getall()
        # for url in pages_url:
        #     yield scrapy.Request(url, callback=self.parse_items)

    def parse_items(self, response):
        items_url = response.css(
            'a.name-link.js-canonical-link::attr(data-href)').getall()
        for url in items_url:
            # yield scrapy.Request(url, callback=self.parse_item)
            yield SplashRequest(
                url, self.parse_item, endpoint='render.html',
                args={'wait': 0.5}
            )

    def parse_item(self, response):
        product_name = response.css(
            'h1.product-name.js-product-name::text').get()
        product_code = response.css(
            'div.product-number > span::text').get()
        product_price = response.css(
            'span.price-sales::text').get().strip()
        color = response.css('span.selected-value::text').get().strip()
        category = response.css(
            'li+li.breadcrumb-item > a > span::text').get()
        description = response.css('li > div > p+p::text').get()
        description = re.sub(re.compile('<.*?>'), '', description)

        sizes = response.css(
            'ul.swatches.size.clearfix > li.selectable > \
            span::text').getall()
        sizes = [size.strip() for size in sizes]
        images = [
            'https://i1.adis.ws/i/boohooamplience/{}_{}_xl'
            .format(product_code.lower(), color)]

        for i in range(1, 4):
            images.append('https://i1.adis.ws/i/boohooamplience/{}_{}_xl_{}'
                          .format(
                              product_code.lower(), color, i))
        colors = response.css(
            'ul.swatches.color.clearfix > li.selectable:not(.selected) > \
            span::attr(data-href)').getall()
        skus = ProductSkus()
        item = Item(product_code=product_code, product_price=product_price,
                    product_name=product_name, product_description=description,
                    product_category=category, product_link=response.url,
                    data_skus=[])
        skus = ProductSkus(color=color, sizes=sizes, pictures=images)
        item["data_skus"].append(skus)
        print(colors)
        # self.items_data[product_code] = {
        #     'Product Name': product_name,
        #     'product Price': product_price,
        #     'description': description,
        #     'category': category,
        #     color: {
        #         'sizes': sizes,
        #         'images': images
        #     }
        # }
        if colors:
            request = SplashRequest(
                colors[0], self.parse_item_color, endpoint='render.html',
                args={'wait': 0.5}
            )
            request.meta['colors'] = colors
            request.meta['item'] = item
            yield request
        else:
            yield item

    def parse_item_color(self, response):
        color = response.css('span.selected-value::text').get().strip()
        product_code = response.css(
            'div.product-number > span::text').get()
        sizes = response.css(
            'ul.swatches.size.clearfix > li.selectable > \
            span::text').getall()
        sizes = [size.strip() for size in sizes]

        images = [
            'https://i1.adis.ws/i/boohooamplience/{}_{}_xl'
            .format(product_code.lower(), color)]

        for i in range(1, 4):
            images.append('https://i1.adis.ws/i/boohooamplience/{}_{}_xl_{}'
                          .format(
                              product_code.lower(), color, i))
        item = response.meta['item']
        skus = ProductSkus(color=color, sizes=sizes, pictures=images)
        item['data_skus'].append(skus)
        # self.items_data[product_code][color] = {
        #     'sizes': sizes,
        #     'images': images
        # }
        colors = response.meta['colors'].remove(response.url)
        if colors:
            request = SplashRequest(
                colors[0], self.parse_item_color, endpoint='render.html',
                args={'wait': 0.5}
            )
            request.meta['colors'] = colors
            request.meta['item'] = item
            yield request
        else:
            yield item
