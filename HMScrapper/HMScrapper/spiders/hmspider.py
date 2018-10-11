"""
HMSpider: A spider written to scrape all items of the H&M
brand's website from link https://kw.hm.com/en/ and store
the scrapped data.
"""
# -*- coding: utf-8 -*-
from HMScrapper.items import HmScrapperItem
from scrapy.linkextractor import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
import HMScrapper.parsing_utilities as util


class HmSpider(CrawlSpider):
    """
    Spider class to scrape categories and follow callbacks to
    GET and POST requests to scrape all the items.
    """
    name = 'hmspider'
    allowed_domains = ['kw.hm.com']
    start_urls = ['https://kw.hm.com/en/']
    rules = [
        Rule(
            LinkExtractor(
                restrict_css="div[class *= 'field__item']",
                canonicalize=True,
                unique=True,
            ),
            callback="parse_item",
        ),
        Rule(
            LinkExtractor(
                restrict_css="li.pager__item",
                canonicalize=True,
                unique=True,
            ),
            follow=True,
        ),
        Rule(
            LinkExtractor(
                restrict_css="li[class *= 'menu--two__list-item']>div",
                canonicalize=True,
                unique=True,
            ),
            follow=True,
        ),
    ]

    @staticmethod
    def parse_item(response):
        """
        Callback for request to parse_item details from product page.
        :param response: response received by hitting the item-url
        :return: Yields item or request for
        scrapping the item-colors if present
        """
        hm_item = HmScrapperItem()
        hm_item['color_skus'] = []
        hm_item['name'] = util.parse_name(response)
        hm_item['price'] = util.parse_price(response)
        hm_item['concept'] = util.parse_concept(response)
        hm_item['discount'] = util.parse_discount(response)
        hm_item['old_price'] = util.parse_old_price(response)
        hm_item['care_info'] = util.parse_care_info(response)
        hm_item['item_code'] = util.parse_item_code(response)
        hm_item['composition'] = util.parse_composition(response)
        hm_item['description'] = util.parse_description(response)
        # Add color skus and yield item
        util.parse_item_color_sku(response, hm_item)
