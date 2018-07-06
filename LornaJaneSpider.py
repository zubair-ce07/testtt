# -*- coding: utf-8 -*-
import scrapy
import math


class LornajaneSpider(scrapy.Spider):

    name = 'LornaJaneSpider'
    allowed_domains = ['lornajane.sg']
    start_urls = ['https://www.lornajane.sg/']
    download_delay = 3

    def parse(self, response):
        cat_urls = self.main_product_links(response)[0]
        yield scrapy.http.Request(cat_urls, callback=self.parse_main_products)

    def parse_main_products(self, response):
        product_links = self.get_sub_prod_links(response)
        product_links = [response.urljoin(href) for href in product_links]

        for product in product_links:
            yield scrapy.http.Request(product, callback=self.parse_products)

        no_of_records = self.records_for_category(response)
        no_of_records = int(no_of_records[-1])
        max_pages = int(math.ceil(no_of_records / 20.0))

        for next_page in range(1, max_pages, 1):
            yield scrapy.http.Request(self.next_page_link(next_page, response), callback=self.parse_main_products)

    def parse_products(self, response):
        item = {
            'care': self.care(response),
            'description': self.description(response),
            'type': self.product_type(response),
            'image_url': self.image_url(response),
            'product_name': self.product_name(response),
            'sku': self.sku_id(response),
            'url': response.url,
            'skus': {}
        }

        yield self.populate_sku_for_all_sizes(item, response)

        color_links = self.color_links(response)
        for color in color_links:
            yield scrapy.http.Request(color, callback=self.parse_products)

    def populate_sku_for_all_sizes(self, item, response):
        for x in self.size(response):
            values = {
                'color': self.color(response),
                'currency': self.currency(response),
                'price': self.price(response),
                'size': x
            }
            item['skus'][item['sku'] + "_" + x + "_" + self.color(response)] = values
        return item

    def main_product_links(self, response):
        links =  response.css('.main-menu > li:nth-child(1) > a:nth-child(1)::attr(href)').extract()
        return [link if 'https://' in link else 'https://www.lornajane.sg{0}'.format(link) for link in links]

    def next_page_link(self, next_page, response):
        return '{0}?page={1}'.format(response.url.split('?')[0], next_page)

    def image_url(self, response):
        return response.urljoin(response.css('.product-slider-image > div.item > picture > source::'
                                             'attr(srcset)')[0].extract())

    def records_for_category(self, response):
            return response.css('.count-text::text').extract()[1].split(' ')

    def get_sub_prod_links(self, response):
        return response.css('div.product-item > div.product-grid-item > div:nth-child(1) > a:nth-child(1)'
                            '::attr(href)').extract()

    def color_links(self, response):
        cols = response.css('.color-swatch > ul:nth-child(1) > li > a.product-detail-swatch-btn'
                            '::attr(data-url)').extract()
        return [('https://www.lornajane.sg{0}').format(col) for col in cols]

    def size(self,response):
        size = response.css('#sizeWrap .product-detail-swatch-btn::text').extract()
        return [s.strip() for s in size]

    def product_name(self, response):
        return response.css('.pro-heading-sec > h1:nth-child(3)::text').extract()[0]

    def color(self, response):
        return response.css('.selected > span::attr(title)').extract()[0].encode('utf-8')

    def product_type(self, response):
        return response.css('.breadcrumb > ul:nth-child(1) > li:nth-child(3) > a:nth-child(1)::'
                            'text').extract()[0].strip()

    def gender(self, response):
        return response.css('female').extract()[0]

    def price(self, response):
        return response.css('div.price:nth-child(4)::text').extract()[1]

    def description(self, response):
        desc = response.css('#desc1 > div.mobile_toggle > div > p:nth-child(3)::text').extract()
        if not desc:
            desc = response.css('#desc1 > div.mobile_toggle > div > p:nth-child(2)::text').extract()
        return desc[0]

    def care(self, response):
        return response.css('div.mobile_toggle:nth-child(1) > ul:nth-child(6) > li::text').extract()

    def sku_id(self, response):
        return response.css('div.mobile_toggle:nth-child(1) > p:nth-child(1)::text').extract()[0].split(':')[1]

    def currency(self, response):
        return response.css('div.price:nth-child(4) > span:nth-child(1)::text').extract()[0]