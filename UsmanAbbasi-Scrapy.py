# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from HypeDC.items import HypedcItem


class HypedcSpider(CrawlSpider):
    name = 'hypedc'
    allowed_domains = ['hypedc.com']
    start_urls = ['http://hypedc.com/brands/']

    rules = (
        Rule(LinkExtractor(allow=(r'\.com/[A-Za-z]*/$'), deny=('news|faq|legals|contacts')),
             follow=True,),
        Rule(LinkExtractor(allow=(r'.*\.html'), deny=('news|faq|legals|contacts')), follow=True, callback='parse_item'),
    )

    def parse_item(self, response):
        item = HypedcItem()
        if response.css('p.addtocart'):
            item['item_id'] = response.css('.product-code::text').extract_first()
            item['url'] = response.url
            item['name'] = response.css('.product-name::text').extract_first()
            item['brand'] = response.css('.product-manufacturer::text').extract_first()
            description = response.css('.product-description.std::text').extract_first()
            item['description'] = description.strip()
            item['color_name'] = response.css('.product-colour::attr(data-bf-color)').extract_first()
            self.image_urls_to_string(response, item)
            self.find_prices(response, item)
        yield item

    def find_prices(self, response, item):
        if response.css('.label-tag.label-tag-lg.label-tag-discount'):
            old_price = response.css('[id^=old-price]::text').extract_first()
            old_price = old_price.strip()
            item['old_price'] = old_price[1:]
            price = response.css('[id^=product-price]::text').extract_first()
            price = price.strip()
            item['price'] = price[1:]
            item['currency'] = price[0]
            item['is_discounted'] = True

        else:
            price = response.css('.price-dollars::text').extract_first() \
                    + response.css('.price-cents::text').extract_first()
            item['is_discounted'] = False
            item['old_price'] = price[1:]
            item['price'] = price[1:]
            item['currency'] = price[0]

    def image_urls_to_string(self, response, item):
        item['image_urls'] = ""
        image_urls_list = response.css('#carousel-product .slides img::attr(src)').extract()
        for url in image_urls_list:
            if r'/750x/' in url:
                item['image_urls'] = url + " " + item['image_urls']

