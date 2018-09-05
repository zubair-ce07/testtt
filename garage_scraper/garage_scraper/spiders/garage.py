# -*- coding: utf-8 -*-
"""
Extracts the details of product list
available on garageclothing.com/ca
"""
import scrapy


class GarageSpider(scrapy.Spider):
    name = 'garage'
    allowed_domains = ['garageclothing.com']
    JSESSIONID = ''

    def start_requests(self):
        yield scrapy.Request(
            url='https://www.dynamiteclothing.com/?postSessionRedirect=https%3A'
            '//www.garageclothing.com/ca&noRedirectJavaScript=true',
            callback=self.pre_parse,
        )

    def pre_parse(self, response):
        """
        Gets response from starts_request and
        extracts JSESSIONID from response.url
        to set self.JESSIONID and then
        generates a request with a callback
        method parse who does the actual
        scraping
        """
        self.JSESSIONID = response.url.split('=')[1]
        yield scrapy.Request(
            url='https://www.garageclothing.com/ca',
            callback=self.parse,
            cookies={
                'JSESSIONID': self.JSESSIONID,
            },
        )

    def parse(self, response):
        urls = response.css('div.zoomitem>a::attr(href)').extract()
        for my_url in urls:
            if my_url:
                my_url = response.urljoin(my_url)
            yield scrapy.Request(
                url=my_url,
                callback=self.parse_cloth,
                cookies={
                    'JSESSIONID': self.JSESSIONID,
                })

    def parse_cloth(self, response):
        yield {
            "name":
            response.css('h1.prodName::text').extract_first(),
            "price":
            response.css('h2.prodPricePDP::text').extract_first(),
            "promo_message":
            response.css('p.promoMessage::text').extract_first(),
            "color":
            response.css('div.swatchColor::text').extract_first(),
            "sizes":
            response.css('div#productSizes span::text').extract(),
            "description":
            response.css('div#descTabDescriptionContent>p::text')
            .extract_first(),
        }
