# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy_splash import SplashRequest


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
        pages_url = response.css(
            '.pagination-item.device-paginate.js-device-paginate > \
            a::attr(href)').getall()
        for url in pages_url:
            yield scrapy.Request(url, callback=self.parse_items)

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

        sizes = response.css(
            'ul.swatches.size.clearfix > li.selectable > \
            span::text').getall()
        sizes = [size.strip() for size in sizes]

        # main = response.css(
        #     '.product-col-1.product-image-container').get()
        # print(main)
        # print(main.css('ul').extract())
        # a.thumbnail-link.js-thumbnail-link::attr(href)
        # for image in images:
        #     print(image)
        colors = response.css(
            'ul.swatches.color.clearfix > li.selectable:not(.selected) > \
            span::attr(data-href)').getall()
        self.items_data[product_code] = {
            'Product Name': product_name,
            'product Price': product_price,
            color: {
                'sizes': sizes
            }
        }
        for url in colors:
            yield SplashRequest(
                url, self.parse_item_color, endpoint='render.html',
                args={'wait': 0.5}
            )

    def parse_item_color(self, response):
        color = response.css('span.selected-value::text').get().strip()
        product_code = response.css(
            'div.product-number > span::text').get()
        sizes = response.css(
            'ul.swatches.size.clearfix > li.selectable > \
            span::text').getall()
        sizes = [size.strip() for size in sizes]
        print(color)
        print(self.items_data[product_code])
        self.items_data[product_code][color] = {
            'sizes': sizes
        }
        print(self.items_data[product_code])
