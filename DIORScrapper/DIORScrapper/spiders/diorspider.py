"""
Spider module to scrape products from
dior.com
"""
# -*- coding: utf-8 -*-
import re
import json
import scrapy
import DIORScrapper.utilities as util
from DIORScrapper.items import DiorItem


class DiorSpider(scrapy.Spider):
    """
    Spider class to scrape products from
    www.dior.com
    """
    name = 'diorspider'
    allowed_domains = ['www.dior.com']
    start_urls = ['https://www.dior.com/en_gb/']

    def parse(self, response):
        """
        Getting page_links from page source and
        yielding requests to parse them all.
        :param response: response obtained by hitting start urls
        :return: GET requests for all product pages
        """
        data = response.css("link+script::text").extract_first()
        pattern = '"href":"(/couture/en_gb/horizon/[a-zA-Z/0-9-’]*)","target"'
        links = re.findall(pattern, data)
        for link in links:
            cat_url = self.start_urls[0] + str(link.split("horizon/")[1])
            cat_url = cat_url.replace("’", "%E2%80%99")
            yield scrapy.Request(cat_url, callback=self.parse_product_page)

    def parse_product_page(self, response):
        """
        Getting all product links and yielding requests to parse
        item details
        :param response: response from hitting product_page_url
        :return: GET requests for all items present on the page
        """
        item_links = response.css("div.product-image>a::attr(href)").extract()
        for link in item_links:
            item_url = response.urljoin(link)
            yield scrapy.Request(item_url, callback=self.parse_product)

    def parse_product(self, response):
        """
        Scrape the item details from JSON data fetched
        from page source and yield the DiorItem.
        :param response: response from hitting item_url
        :return: DiorItem
        """
        item = DiorItem()
        json_string = response.css("link+script::text").extract_first()
        json_data = json.loads(json_string.split("State = ")[1].strip())
        item_data = json_data['CONTENT']

        item['url'] = response.url
        item['id'] = util.parse_id(item_data)
        item['name'] = util.parse_name(item_data)
        item['sizes'] = util.parse_sizes(item_data)
        item['brand'] = util.parse_brand(item_data)
        item['price'] = util.parse_price(item_data)
        item['colors'] = util.parse_colors(item_data)
        item['status'] = util.parse_status(item_data)
        item['variant'] = util.parse_variant(item_data)
        item['category'] = util.parse_category(item_data)
        item['image_urls'] = util.parse_image_urls(item_data)

        yield item
