# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider


class Hypedc2Spider(CrawlSpider):
    name = 'hypedc2'
    allowed_domains = ['hypedc.com']
    start_urls = [
        'https://www.hypedc.com/mens/',
        'https://www.hypedc.com/womens/',
        'https://www.hypedc.com/kids/'
    ]
    rules = (
        Rule(LinkExtractor(
            restrict_css="a.next.btn.btn-primary")),
        Rule(LinkExtractor(
            restrict_css='div.item.col-xs-12.col-sm-6>a'), callback='parse_details'),
    )

    def parse_details(self, response):
        yield {

            # 'item_id': response.css('').extract(),
            'url': response.url,
            'name': response.css('h1.product-name::attr(data-bf-productname)').extract(),
            'brand': response.css('h2.product-manufacturer::text').extract(),
            'description': response.css('div.product-description.std::text').extract(),
            'currency': response.css('h2.product-price>meta::attr(content)').extract(),
            # 'is_discounted': response.css('').extract(),
            'price': response.css('h2.product-price::attr(data-bf-productprice)').extract(),
            # 'old_price': response.css('').extract(),
            'color_name': response.css('h3.h4.product-colour::attr(data-bf-color)').extract(),
            'image_urls': response.css('img.img-responsive.unveil::attr(data-src)').extract(),


        }
