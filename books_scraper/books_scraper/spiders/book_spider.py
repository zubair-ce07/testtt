# -*- coding: utf-8 -*-
"""
Scraps details of each book available
on each page following hyperlinks
"""
import scrapy

from items import BooksScraperItem


class BookScraperSpider(scrapy.Spider):
    name = 'book_spider'
    allowed_domains = ['toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        """
        Scraps all the available
        hyperlinks of the books.
        """
        urls = response.css(
            'section li[class*="col-xs-6"]>article.product_pod h3>a::attr(href)'
        ).extract()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_book_details)

        # pagination
        next_page_url = response.css('li.next > a::attr(href)').extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_book_details(self, response):
        """
        Scraps the details of book
        available on the page.
        """
        book = BooksScraperItem()
        keys = response.css('article.product_page table th::text').extract()
        values = response.css('article.product_page table td::text').extract()
        dictionary = dict(zip(keys, values))

        book["title"] = response.css(
            'div.page_inner > ul.breadcrumb li.active::text').extract_first()
        book["category"] = response.css(
            'div.page_inner > ul.breadcrumb li>a::text').extract()[2]
        book["description"] = response.css(
            'div#product_description + p::text').extract()
        book["product_information"] = dictionary
        book["rating"] = response.css(
            'div.product_main > p.star-rating::attr(class)').extract_first(
            ).split()[1]
        book["price"] = response.css(
            'div.product_main p.price_color::text').extract()

        yield book
