# -*- coding: utf-8 -*-
import scrapy


class OrsaySpider(scrapy.Spider):
    name = 'orsay.com'
    allowed_domains = ['orsay.com']
    start_urls = ['http://www.orsay.com/de-de/']
    download_delay = 3

    def parse(self, response):
        cat_urls = self.main_product_links(response)
        for category in cat_urls:
            yield scrapy.http.Request(category, callback=self.parse_main_products)

    def parse_main_products(self, response):
        product_links = self.get_sub_prod_links(response)
        product_links = [response.urljoin(href) for href in product_links]

        for product in product_links:
            yield scrapy.http.Request(product, callback=self.parse_products)

        no_of_records = self.records_for_category(response)
        for next_page in range(12, int(no_of_records)-12, 12):
            yield scrapy.http.Request(self.next_page_link(next_page, response), callback=self.parse_main_products)

    def parse_products(self, response):

        item = {
            'care': self.care(response),
            'description': self.description(response),
            'type': self.product_type(response),
            'Product_name': self.product_name(response),
            'url': response.url,
            'image_url': self.image_url(response),
            'sku': self.sku_id(response),
            'skus': {}
        }
        yield self.populate_sku_for_all_sizes(item, response)
        color_links = self.color_links(response)
        for color in color_links:
            yield scrapy.http.Request(color, callback=self.parse_products)

    def image_url(self, response):
        return response.css('.product-col-1 > div.js-slick-swiper > div > img::attr(src)').extract()[0]

    def stock(self, idx, response):
        stock_list = response.css('.size > li::attr(class)').extract()
        return 'Out of Stock' if 'unselectable' in stock_list[idx]  else 'In Stock'

    def next_page_link(self, next_page, response):
        return '{0}?sz=12&start={1}'.format(response.url.split('?sz=')[0], next_page)

    def care(self, response):
        return response.css('.product-material > p:nth-child(2)::text').extract()[0]

    def main_product_links(self, response):
        return response.css('.header-navigation > ul a.has-sub-menu.'
                            'level-1.visible-xlg::attr(href)').extract()[0:4]

    def description(self, response):
        name = response.css('.js-product-content-gtm::attr(data-product-details)').extract()[0].split(',')
        name = [d for d in name if 'name' in d]
        return name[0].split(':')[1][1:-1]

    def populate_sku_for_all_sizes(self, item, response):
        for idx, siz in enumerate(self.size(response)):
            values = {'color': self.color(response),
                      'currency': self.currency(response),
                      'price': self.price(response),
                      'stock': self.stock(idx, response),
                      'size': siz}
            item['skus'][item['sku'] + "_" + siz] = values
        return item

    def records_for_category(self, response):
        return response.css('div.refinements-footer > div > div.pagination-product-count'
                            '::attr(data-count)').extract()[0]

    def get_sub_prod_links(self, response):
        return response.css('.product-image a.thumb-link::attr(href)').extract()

    def size(self, response):
        size = response.css('.size li a::text').extract()
        return [s.strip() for s in size]

    def price(self, response):
        return response.css('.price-sales::text').extract()[0].strip().split(' ')[0]

    def color(self, response):
        return response.css('.color li.selectable.selected a.swatchanchor::attr(title)').extract()[0].strip().split(' - ')[1]

    def color_links(self, response):
        return response.css('.color li a.swatchanchor::attr(href)').extract()

    def currency(self, response):
        curr = response.css('.js-product-content-gtm::attr(data-product-details)').extract()[0].split(',')
        return curr[-2].split(':')[-1][1:-1]

    def sku_id(self, response):
        return response.css('div.tooltip-wrapper:nth-child(3) > div:nth-child(2)::text').extract()[0].split('. ')[1]

    def product_name(self, response):
        return response.css('#product-content h1::text').extract()[0]

    def product_type(self, response):
        return response.css('div > div.breadcrumb > a:nth-child(3) > span::text').extract()[0].strip()
