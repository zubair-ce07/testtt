"""
This module crawl pages and get data.
"""
import re
import scrapy


class OrsaySpider(scrapy.Spider):
    """This class crawl orsay pages"""
    name = 'orsay'

    def start_requests(self):
        """This method request for crawl orsay pages"""
        start_urls = 'http://orsay.com'
        yield scrapy.Request(url=start_urls, callback=self.parse)

    def parse(self, response):
        """This method crawl page urls."""
        for url in response.css('div.header-in>nav>ul>li'):

            for link2 in url.css(
                    'div.js-menu-item-content>div.navigation-content-in>\
                    ul.navigation-vertical>li.navigation-column>ul>li>a::attr(href)').extract():
                data1 = {
                    'url': link2,
                }
                request = scrapy.Request(
                    url=link2, callback=self.get_unique_urls)
                request.meta['url'] = data1
                yield request

            for link3 in url.css('div.js-menu-item-content>ul>li>a::attr(href)').extract():
                data2 = {
                    'url': link3,
                }
            request = scrapy.Request(
                url='', callback=self.get_unique_urls)
            request.meta['url'] = data2
            yield request

    def get_unique_urls(self, response):
        """This method crawl useful information."""
        link = response.meta['url']

        for item in response.css('li.grid-tile'):
            detail_info_url = item.css(
                'div.product-image>a::attr(href)').extract_first()
            price = item.css(
                'div.product-swatches>ul>li>a::attr(data-prices)').extract_first()
            item_details = {
                'url': detail_info_url,
                'item_title': item.css(
                    'div.product-swatches>ul>li>a::attr(title)').extract_first(),
                'item_price': price,
                'item_sizes': item.css('span.size-selectable>a::text').extract(),
            }
            detail_info_url = response.urljoin(detail_info_url)
            request = scrapy.Request(
                url=detail_info_url, callback=self.parse_product_description)
            request.meta['data'] = link
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
            'url': item_details['url'],
            'desc_url': data,
            'item_title': item_details['item_title'],
            'item_price': item_details['item_price'],
            'item_sizes': item_details['item_sizes'],
            'item_description': modified_description,
        }
        yield product_details
