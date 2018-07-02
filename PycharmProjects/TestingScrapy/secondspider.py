# -*- coding: utf-8 -*-
import scrapy


class SecondSpider(scrapy.Spider):
    name = 'secondspider'
    allowed_domains = ['www.orsay.com']
    start_urls = ['https://www.orsay.com/de-de/']
    download_delay = 3

    def __init__(self):
        self.sku = {}
        self.skus = {}
        self.count = 0

    def parse(self, response):
        list_product_cat = response.css('#wrapper > header > div > nav > ul > li > div > '
                                        'div > ul > li.navigation-column > ul > li > a::text').extract()
        list_product_cat = [x.strip().encode('utf8') for x in list_product_cat]
        list_product_cat = list(set(list_product_cat))

        for x in list_product_cat:
            self.sku[x] = []

        list_product_link = {'product_links': response.css('.header-navigation > ul:nth-child(1) '
                                                           'li.js-accordion-item.js-menu-item a.has-sub-menu.'
                                                           'navigation-link.level-1.visible-xlg::attr(href)').extract()}
        list_product_link['product_links'].pop(4)
        yield scrapy.http.Request(list_product_link['product_links'].pop(0), callback=self.parse_main_products_callback,
                                  method='GET', meta={'list_product_link': list_product_link['product_links']},
                                  dont_filter=True)

    def parse_main_products_callback(self, response):
        item = {
            'sub_product_links': response.css('.product-image a.thumb-link::attr(href)').extract(),
        }
        no_of_records = response.css('#secondary > div > div.refinements-footer > div > div.'
                                     'pagination-product-count.js-pagination-product-count'
                                     '::attr(data-count)').extract()
        if len(no_of_records):
            no_of_records = no_of_records[0].encode('utf-8')
            i = 0
            while i < int(no_of_records) / 12:
                response.meta['list_product_link'].append(response.url + '/?sz=12&start=' + str(12 + i * 12) +
                                                          '&format=page-element')
                i += 1

        item['sub_product_links'] = [("http://www.orsay.com" + x) for x in item['sub_product_links']]
        list_prod_link = response.meta['list_product_link']

        if len(item['sub_product_links']):
            yield scrapy.http.Request(item['sub_product_links'].pop(0), callback=self.parse_sub_products_callback,
                                      method='GET', meta={'product_links': item['sub_product_links'],
                                                          'list_prod_cat': list_prod_link}, dont_filter=True)

        if response.meta['list_product_link']:
            yield scrapy.http.Request(list_prod_link.pop(0), callback=self.parse_main_products_callback,
                                      method='GET', meta={'list_product_link': list_prod_link}, dont_filter=True)

    def parse_sub_products_callback(self, response):
        item = {
            'type': response.css('#main > div.container > div > div.breadcrumb > a:nth-child(3) > '
                                 'span::text').extract()[0].strip(),
            'product_name': response.css('#product-content h1::text').extract(),
            'sku': response.css('div.tooltip-wrapper:nth-child(3) > div:nth-child(2)::text').extract()[0].split('. ')[1],
            'currency': response.css('.header-localization > div:nth-child(2) > div:nth-child(2) > a:nth-child(1) > '
                                     'span:nth-child(2) > span:nth-child(2)::text').extract(),
            'color_links': response.css('.color li a.swatchanchor::attr(href)').extract(),
            'color': response.css('.color li a.swatchanchor::attr(title)').extract(),
            'price': response.css('.price-sales::text').extract(),
            'size': response.css('.size li a::text').extract(),
        }

        for x in item['size']:
            values = {'color': item['color'][0].encode("utf-8").strip().split(' - ')[1],
                      'currency': item['currency'][0].encode("utf-8").strip(),
                      'price': item['price'][0].encode("utf-8").strip().split(' ')[0],
                      'size': x.encode("utf-8").strip()}
            self.skus[item['sku'].encode("utf-8") + "_" + x.encode("utf-8").strip()] = values

        if item['type']:
            self.sku[item['type']].append(self.skus)

        prod_links = response.meta['product_links']

        if len(item['color_links']):
            yield scrapy.http.Request(item['color_links'].pop(0), callback=self.parse__same_prod_variant_callback,
                                      method='GET', meta={'color_links': item['color_links'],
                                                          'product_links': prod_links})

        if prod_links:
            yield scrapy.http.Request(prod_links.pop(0), callback=self.parse_sub_products_callback,
                                      method='GET', meta={'product_links': prod_links})

    def parse__same_prod_variant_callback(self, response):
        item = {
            'type':
                response.css('#main > div.container > div > div.breadcrumb > a:nth-child(3) > span::text').extract()[
                    0].strip(),
            'sku': response.css('div.tooltip-wrapper:nth-child(3) > div:nth-child(2)::text').extract()[0].split('. ')[
                1],
            'currency': response.css('.header-localization > div:nth-child(2) > div:nth-child(2) > a:nth-child(1) > '
                                     'span:nth-child(2) > span:nth-child(2)::text').extract()[0].encode("utf-8"),
            'color': response.css('.color li.selectable.selected a.swatchanchor.js-color-swatch::attr(title)')
                .extract()[0].encode("utf-8").split('- ')[1],
            'price': response.css('.price-sales::text').extract()[0].encode("utf-8").strip().split(" ")[0],
            'size': response.css('.size li a::text').extract(),
        }

        for x in item['size']:
            values = {'color': item['color'],
                      'currency': item['currency'],
                      'price': item['price'],
                      'size': x.encode("utf-8").strip()}
            self.skus[item['sku'].encode("utf-8") + "_" + x.encode("utf-8").strip()] = values

        if item['type']:
            self.sku[item['type']].append(self.skus)

        colorLink = response.meta['color_links']
        if colorLink:
            return scrapy.http.Request(colorLink.pop(0), callback=self.parse__same_prod_variant_callback,
                                       method='GET', meta={'color_links': colorLink}, dont_filter=True)
