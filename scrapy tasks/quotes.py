"""
This module crawl pages and get data.
"""
# -*- coding: utf-8 -*-
import re
import scrapy


class QuotesSpider(scrapy.Spider):
    """This class crawl quotes pages"""
    name = 'quotes'
    allowed_domains = ['toscrape.com']
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        """This method crawl page and store useful information."""
        for quote in response.css('div.quote'):
            quote_text = quote.css('span.text::text').extract_first()
            pattern = "([^\t\r\f\v\"]*[a-z.,&A-Z0-9 ]*\w+)"
            quote_text = re.match(pattern, quote_text, flags=re.DOTALL)
            author_name = quote.css('small.author::text').extract_first()
            author_name = re.match(pattern, author_name, flags=re.DOTALL)
            detail_url = str(quote.css('span > a::attr(href)').extract_first())
            detail_page_url = response.urljoin(detail_url)
            data = {
                'text': quote_text.group(),
                'author_name': author_name.group(),
                'tags': quote.css('a.tag::text').extract(),
                'about_url': quote.css('span > a::attr(href)').extract_first(),
            }
            request = scrapy.Request(
                url=detail_page_url, callback=self.parse_details)
            request.meta['data'] = data
            yield request

        next_page_url = response.css('li.next > a::attr(href)').extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_details(self, response):
        """This method stores author detail information."""
        data = response.meta['data']
        pattern = "([a-z: (\".'-=,&)A-Z0-9 ]*\w+)"
        text = response.css('div.author-description::text').extract_first().strip()
        text = re.match(pattern, text, flags=re.DOTALL)
        author_name = response.css('h3.author-title::text').extract_first()
        author_name = re.match(pattern, author_name, flags=re.DOTALL)
        author_name = author_name.group()
        detail_data = {
            'name': author_name,
            'birth-date': response.css('span.author-born-date::text').extract_first(),
            'description': text.group(),
        }
        data = {
            'quote_data': data,
            'author_detail': detail_data
        }
        yield data
