"""Boohooman scrapper module.

This module scrap all the items from boohoman website and store it in a json
file
"""
import re

import scrapy

from boohooman.items import Item, ProductSkus


class BoohooManSpider(scrapy.Spider):
    """This is scrapper class for boohooman scrapper.

    This class have differnet methods that scrap each part of the website.
    """

    name = 'boohoo_man'
    allowed_domains = ['www.boohooman.com']
    start_urls = ['https://www.boohooman.com/']
    items_data = {}

    def parse(self, response):
        """Scrap clothing menu.

        This method scrap clothing menu and extract links from it and then
        call parse_pages on those links
        """
        clothing = response.xpath(
            "//li['@class=has-submenu js-has-submenu js-prevent-event \
            js-menu-tab' and ./a[contains(.,'CLOTHING')]]")
        heading_urls = clothing.css(
            '.menu-vertical.js-menu-vertical > li > a::attr(href)').getall()
        for url in heading_urls:
            yield scrapy.Request(url, callback=self.parse_pages)

    def parse_pages(self, response):
        """Scrap pages of a menu.

        This method extract all the pages links for a menu and
        then call parese_items on those links
        """
        yield scrapy.Request(
            response.url, callback=self.parse_items, dont_filter=True)
        pages_url = response.css(
            '.pagination-item.device-paginate.js-device-paginate > \
            a::attr(href)').getall()
        for url in pages_url:
            yield scrapy.Request(url, callback=self.parse_items)

    def parse_items(self, response):
        """Scrap items from a page.

        This method extract all the links of the items in a page
        """
        items_url = response.css(
            'a.name-link.js-canonical-link::attr(data-href)').getall()
        for url in items_url:
            yield scrapy.Request(
                url, callback=self.parse_item)

    def parse_item(self, response):
        """Scrap item from a page.

        This method extract all data of an item from a page
        """
        item = self.make_item(response)
        colors = response.css(
            'ul.swatches.color.clearfix > li.selectable:not(.selected) > \
            span::attr(data-href)').getall()

        if colors:
            request = scrapy.Request(
                colors[0], callback=self.parse_item_color)
            request.meta['colors'] = colors
            request.meta['item'] = item
            yield request
        else:
            yield item

    def parse_item_color(self, response):
        """Parse item with aother color.

        This method will be callled if an item has more than one color then
        this will be called recursively for that item until all the colors
        data is extracted
        """
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
        colors = response.meta['colors'].remove(response.url)
        if colors:
            request = scrapy.Request(
                colors[0], callback=self.parse_item_color)
            request.meta['colors'] = colors
            request.meta['item'] = item
            yield request
        else:
            yield item

    def make_item(self, response):
        """Extract item from a response.

        This method extract all data of an item from a response and then
        return it
        """
        item = Item()
        item['product_link'] = response.url
        item['product_code'] = response.css(
            'div.product-number > span::text').get()
        item['product_name'] = response.css(
            'h1.product-name.js-product-name::text').get()
        item['product_price'] = response.css(
            'span.price-sales::text').get().strip()
        item['product_category'] = response.css(
            'li+li.breadcrumb-item > a > span::text').get()
        color = response.css('span.selected-value::text').get().strip()

        description = response.css(
            '#product-short-description-tab > div > p+p').get()
        if description:
            item['product_description'] = description
            item['product_description'] = re.sub(re.compile(r'<[^>]+>'), '',
                                                 item['product_description'])
        item['data_skus'] = []

        print("Processing : {}".format(item['product_name']))

        sizes = response.css(
            'ul.swatches.size.clearfix > li.selectable > \
            span::text').getall()
        sizes = [size.strip() for size in sizes]
        images = [
            'https://i1.adis.ws/i/boohooamplience/{}_{}_xl'
            .format(item['product_code'].lower(), color)]

        for i in range(1, 4):
            images.append('https://i1.adis.ws/i/boohooamplience/{}_{}_xl_{}'
                          .format(
                              item['product_code'].lower(), color, i))
        skus = ProductSkus(color=color, sizes=sizes, pictures=images)
        item["data_skus"].append(skus)

        return item
