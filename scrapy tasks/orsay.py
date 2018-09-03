"""
This module crawl pages and get data.
"""
# -*- coding: utf-8 -*-
import re
import scrapy


class OrsaySpider(scrapy.Spider):
    """This class crawl orsay pages"""
    name = 'orsay'
    allowed_domains = ['orsay.com']
    start_urls = ['http://orsay.com']

    def parse(self, response):
        """This method crawl page and store useful information."""
        link_url = response.css(
            'div.header-in>nav>ul>li>a::attr(href)').extract()
        for url in link_url:
            request = scrapy.Request(url=url, callback=self.parse_details)
            request.meta['url'] = url
            yield request

    def parse_details(self, response):
        """This method crawls product urls and detail information."""
        data = response.meta['url']
        for item in response.css('li.grid-tile'):
            detail_info_url = item.css(
                'div.product-image>a::attr(href)').extract_first()
            price = item.css(
                'div.product-swatches>ul>li>a::attr(data-prices)').extract_first()
            item_details = {
                'item_description_url': detail_info_url,
                'item_title': item.css(
                    'div.product-swatches>ul>li>a::attr(title)').extract_first(),
                'item_price': price.replace('\"', '').replace('null', '0'),
                'item_sizes': item.css('span.size-selectable>a::text').extract(),
            }
            detail_info_url = response.urljoin(detail_info_url)
            request = scrapy.Request(
                url=detail_info_url, callback=self.parse_product_description)
            request.meta['data'] = data
            request.meta['item_details'] = item_details
            yield request

    def parse_product_description(self, response):
        """This method gets product description."""
        data = response.meta['data']
        item_details = response.meta['item_details']
        pattern = "([-]*[a-z:,A-Z0-9% ]*)"
        description = response.css(
            'div.product-info-block>div.js-collapsible>div::text').extract()
        modified_description = []
        for point in description:
            if point is not '\n':
                point = re.match(pattern, point, flags=re.DOTALL)
                if point is not '':
                    modified_description.append(point.group())
                else:
                    pass
            else:
                pass

        product_details = {
            'Category_url': data,
            'item_details': item_details,
            'item_description': modified_description,
        }
        yield product_details
