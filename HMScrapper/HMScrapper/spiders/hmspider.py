"""
HMSpider: A spider written to scrape all items of the H&M
brand's website from link https://kw.hm.com/en/ and store
the scrapped data.
"""
# -*- coding: utf-8 -*-
import json
import scrapy
from lxml import html
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
            LinkExtractor(restrict_css="div[class *= 'field__item']",),
            callback="parse_item",
        ),
        Rule(
            LinkExtractor(restrict_css="li.pager__item",),
        ),
        Rule(
            LinkExtractor(
                restrict_css="li[class *= 'menu--two__list-item']>div",
            ),
        ),
    ]

    def parse_item(self, response):
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
        color_codes = util.parse_color_codes(response)
        if not color_codes:
            yield hm_item
        else:
            request_data = util.prepare_parse_color_request(response,
                                                            color_codes,
                                                            hm_item)
            yield scrapy.FormRequest(url=request_data['url'],
                                     method='POST',
                                     callback=self.parse_color,
                                     headers=request_data['header'],
                                     meta=request_data['meta'],
                                     formdata=request_data['form_data'],
                                     dont_filter=True)

    def parse_color(self, response):
        """
        Callback function to scrape item color and size information.
        :param response: response received by POST request of an item.
        :return: yields the item after scrapping the color
        and size information of the item.
        """
        # get meta data from response
        hm_item = response.meta['item']
        color_codes = response.meta['color_codes']
        data = json.loads(response.body)
        for value in data:
            if 'replaceDynamicParts' in value.values():
                html_value = html.fromstring(value['args'][0]['replaceWith'])
                color_code = util.get_color_from_html(html_value)
                sizes = util.get_sizes_from_html(html_value)
                color_sku = {
                    'color_code': color_code,
                    'sizes': sizes,
                }
                # append the color_sku to item
                hm_item['color_skus'].append(color_sku)
        # if more colors are left
        if not color_codes:
            yield hm_item
        else:
            header = response.meta['header']
            form_data = response.meta['data']
            form_data['configurables[article_castor_id]'] = color_codes[0]
            # create meta for next request
            meta = {
                'item': hm_item,
                'header': header,
                'data': form_data,
                'color_codes': color_codes[1:],
            }
            # yield request for next color
            yield scrapy.FormRequest(url=response.url,
                                     method='POST',
                                     callback=self.parse_color,
                                     headers=header,
                                     meta=meta,
                                     formdata=form_data,
                                     dont_filter=True)
