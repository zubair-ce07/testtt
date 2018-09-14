"""
This module crawl pages and get data.
"""
import re
import scrapy


class DeMart(scrapy.Spider):
    """This class crawl Sheego pages"""
    name = 'demart'

    def start_requests(self):
        """This method request for crawl orsay pages"""
        start_urls = 'http://www.demart.com.pl/'
        yield scrapy.Request(url=start_urls, callback=self.parse)

    def parse(self, response):
        """This method crawl page urls."""
        category_url = response.css('li>a::attr(href)').extract()
        for link in category_url:
            url = response.urljoin(link)
            yield scrapy.Request(
                url=url, callback=self.item_info_url)

    def item_info_url(self, response):
        """This method crawl item detail url."""
        item_url = response.css('div.right>a::attr(href)').extract()
        for link in item_url:
            url = response.urljoin(link)
            yield scrapy.Request(
                url=url, callback=self.item_detail)

    def item_detail(self, response):
        """This method crawl item details."""
        pattern = "[a-zA-z]*"
        information = []
        description = response.css(
            'div.product_right>div.trunc>p::text').extract()
        concatinate_description = ''.join(description)
        description = concatinate_description.strip()
        info = response.css('div.info>div>p::text').extract()
        data_found = response.css('div.info>div>p>strong::text').extract()
        series = response.css('div.info>div>p>a::text').extract_first()
        for index, source_data in enumerate(info):
            # storing data in list that is fetched.
            key = data_found[index].strip()
            key = re.match(pattern, key)
            other_info = {
                key.group(): source_data.strip(),
            }
            information.append(other_info)
        if series:
            series = series.strip()
        else:
            series = 'None'
        data = {
            'item_detail_link': response.url,
            'title': response.css(' h1.product::text').extract_first().strip(),
            'informaton': information,
            'series': series,
            'description': description,
        }
        yield data
