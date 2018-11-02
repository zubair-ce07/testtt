"""
This module scraps the data of Ernstings-Family website
It scraps all the products from the website using scrapy
and creates the data.csv file
"""
# -*- coding: utf-8 -*-
import json
import scrapy
from ErnStingScrapper.items import ErnStingItem
from scrapy.linkextractor import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from ErnStingScrapper import parsing_utilities as util


class ErnStingSpider(CrawlSpider):
    """
    Spider class to scrape products from ErnSting's website
    """
    name = 'spider'
    start_urls = ['https://www.ernstings-family.de/']
    rules = [
        Rule(
            LinkExtractor(
                restrict_css=".main-navigation-inner-wrapper li",
            ),
        ),
        Rule(
            LinkExtractor(
                restrict_css="li[class *= 'item-level1']",
            ),
            callback="parse_filter_page",
        ),
        Rule(
            LinkExtractor(
                restrict_css="li[class *= 'special-list-item']",
            ),
            callback="parse_filter_page",
        ),
    ]

    def parse_filter_page(self, response):
        """
        Yields requests for all pages of a sub-category
        to parse items from
        :param response: sub-category page response to parse
        :return: Requests to parse items from pages
        """
        page_urls = util.get_page_urls(response)
        for url in page_urls:
            yield scrapy.Request(url=url,
                                 callback=self.parse_items_from_json,)

    def parse_items_from_json(self, response):
        """
        parse json object received in callback to retrieve
        products per page.
        :param response: response object containing products per page
        :return: Yields product Items
        """
        # json object containing per page items
        data = json.loads(response.body)
        # it will be parsed to obtain all fields of an Item
        items = data['CatalogEntryView']
        for item in items:
            product = ErnStingItem()
            product['url'] = util.parse_item_url(item)
            product["labels"] = util.parse_labels(item)
            product['skus'] = util.parse_item_skus(item)
            product['name'] = util.parse_item_name(item)
            product['colors'] = util.parse_item_colors(item)
            product['detail'] = util.parse_item_detail(item)
            product['image_urls'] = util.parse_image_paths(item)
            product['material'] = util.parse_item_material(item)
            yield product
