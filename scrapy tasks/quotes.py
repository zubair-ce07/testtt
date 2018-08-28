"""
This module crawl pages and get data.
"""
# -*- coding: utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):
    """This class crawl quotes pages"""
    name = 'quotes'
    allowed_domains = ['toscrape.com']
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        """This method crawl page and store useful information."""
        for quote in response.css('div.quote'):
            data = {
                'text': quote.css('span.text::text').extract_first(),
                'author_name': quote.css('small.author::text').extract_first(),
                'tags': quote.css('a.tag::text').extract(),
                'about': quote.css('span > a::attr(href)').extract_first(),
            }
            yield data
        detail_url = response.css('span > a::attr(href)').extract()
        for url in detail_url:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_details)

        next_page_url = response.css('li.next > a::attr(href)').extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_details(self, response):
        """This method stores author detail information."""
        detail_data = {
            'name': response.css('h3.author-title::text').extract_first(),
            'birth-date': response.css('span.author-born-date::text').extract_first(),
            'description': response.css('div.author-description::text').extract_first(),
        }
        yield detail_data
