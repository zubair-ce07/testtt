# -*- coding: utf-8 -*-
import scrapy


class OrsaySpider(scrapy.Spider):
    name = 'orsay.com'
    allowed_domains = ['orsay.com']
    start_urls = ['http://www.orsay.com/de-de/']
    download_delay = 3

    def parse(self, response):
        list_product_link = {'product_links': self.main_product_links(response)}
        for category in list_product_link['product_links']:
            yield scrapy.http.Request(category, callback=self.parse_main_products, method='GET')

    def parse_main_products(self, response):
        item = {'sub_product_links': self.get_sub_prod_links(response),'next_page': []}
        item['sub_product_links'] = [("http://www.orsay.com" + x) for x in item['sub_product_links']]
        no_of_records = self.records_for_category(response)
        if len(no_of_records):
            no_of_records = int(no_of_records[0].encode('utf-8'))
            for i in range(0, no_of_records, 12): 
                item['next_page'].append(('{0}?sz=12&start={1}&format=page-element').format(response.url,i))

        for product in item['sub_product_links']:
            yield scrapy.http.Request(product, callback=self.parse_sub_products_callback, method='GET')

        for next_page in item['next_page']:
            yield scrapy.http.Request(next_page, callback=self.parse_main_products, method='GET')

    def parse_sub_products_callback(self, response):
        item = {
            'care' : self.care(response),
            'description': self.description(response),
            'type': self.product_type(response),
            'Product_name': self.product_name(response),
            'sku': self.sku_id(response),
            'skus': {}
        }
        for x in self.size(response):
            values = {'color': self.color(response),
                      'currency': self.currency(response),
                      'price': self.price(response),
                      'size': x}
            item['skus'][item['sku'] + "_" + x] = values
        yield item
        color_links = self.color_links(response)
        for color in color_links:
            yield scrapy.http.Request(color, callback=self.parse_sub_products_callback, method='GET')

    def care(self, response):
        return response.css('.product-material > p:nth-child(2)::text').extract()[0].encode('utf-8')

    def main_product_links(self, response):
        return response.css('.header-navigation > ul a.has-sub-menu.'
                            'level-1.visible-xlg::attr(href)').extract()[0:4]

    def description(self, response):
        name = response.css('#product-content > div.js-product-content-gtm::attr(data-product-details)').extract()[
            0].split(',')
        name = [d for d in name if 'name' in d]
        return name[0].encode('utf-8').split(':')[1][1:-1]

    def records_for_category(self, response):
        return response.css('div.refinements-footer > div > div.pagination-product-count'
                            '::attr(data-count)').extract()

    def get_sub_prod_links(self, response):
        return response.css('.product-image a.thumb-link::attr(href)').extract()

    def size(self, response):
        size = response.css('.size li a::text').extract()
        return [s.encode('utf-8').strip() for s in size]

    def price(self, response):
        return response.css('.price-sales::text').extract()[0].encode("utf-8").strip().split(' ')[0]

    def color(self, response):
        return response.css('.color li.selectable.selected a.swatchanchor::attr(title)').extract()[0].encode("utf-8").strip().split(' - ')[1]

    def color_links(self, response):
        return response.css('.color li a.swatchanchor::attr(href)').extract()

    def currency(self, response):
        return response.css('.header-localization > div:nth-child(2) > div:nth-child(2) > a:nth-child(1) > '
                            'span:nth-child(2) > span:nth-child(2)::text').extract()[0].encode("utf-8").strip()

    def sku_id(self, response):
        return response.css('div.tooltip-wrapper:nth-child(3) > div:nth-child(2)::text').extract()[0].split('. ')[1].encode("utf-8")

    def product_name(self, response):
        return response.css('#product-content h1::text').extract()[0].encode("utf-8")

    def product_type(self, response):
        return response.css('div > div.breadcrumb > a:nth-child(3) > span::text').extract()[0].strip().encode('utf-8')
