# -*- coding: utf-8 -*-
"""
this modeule contain a scrapy spider that scrape the whole Boohooman.com website
"""

import json
from functools import partial
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from boohooman_scraping.items import Product, ProductSku


class BoohoomanSpider(CrawlSpider):
    """
    this class is scrapy spider
    """
    name = 'boohooman'
    allowed_domains = ['www.boohooman.com']
    start_urls = ['https://www.boohooman.com']
    images_domain = 'https://i1.adis.ws/i/boohooamplience/'

    nav_link_extractor = LinkExtractor(restrict_css="ul.menu-vertical a")
    pagination_link_extractor = LinkExtractor(restrict_css="li.pagination-item-next a")
    rules = (
        Rule(nav_link_extractor, callback='parse_main_pages', follow=True),
        Rule(pagination_link_extractor, callback='parse_main_pages', follow=True),

    )

    def parse_main_pages(self, response):
        """
        this callback parse main page and category pages
        :param response:
        :return:
        """
        for item in response.css('div.product-tile'):
            item_url = item.css('div.product-name a::attr(href)').extract_first()
            yield scrapy.Request(url=item_url, callback=self.parse_item)

    def parse_item(self, response):
        """
        this method parse the product detail of each product and store in item
        :param response:
        :return:
        """
        product_detail_json = json.loads(
            response.css('form.pdpForm::attr(data-product-details)').extract_first())

        product = Product()
        product['name'] = product_detail_json['name']
        product['retailer_sku'] = product_detail_json['id'].lower()

        product['category'] = []
        product['category'].append(product_detail_json['category'])
        if product_detail_json['dimension60']:
            product['category'].append(product_detail_json['dimension60'])
        if product_detail_json['dimension62']:
            product['category'].append(product_detail_json['dimension62'])

        product['brand'] = product_detail_json['brand']
        product['price'] = response.css('span.price-sales::attr(content)').extract_first()
        product['currency'] = response.css("div.product-price meta::attr(content)").extract_first()
        product['url'] = response.url
        product['merch_info'] = []
        merch_info = response.css('div.product-promo-msg::text').extract_first().strip('\n')
        product['merch_info'].append(merch_info)

        color_urls = response.css('ul.color span.swatchanchor::attr(data-href)').extract()
        product['skus'] = {}
        product['image_urls'] = []
        last_color_flag = False
        for color_url in color_urls:
            if color_url == color_urls[-1]:
                last_color_flag = True
            color_url = color_url + "&format=json"
            request = scrapy.Request(url=color_url,
                                     callback=partial(self.parse_item_colors, product=product,
                                                      last_color_flag=last_color_flag))
            yield request

    def parse_item_colors(self, response, product=None, last_color_flag=False):
        """
        this method take an item object and store skus in it according to color and size
        :param response:
        :param product:
        :param last_color_flag:
        :return:
        """
        sizes = response.css('ul.size li.selectable span::text').extract()

        color = response.css(
            'ul.color li.selected span.swatchanchor::attr(data-variation-values)').extract_first()
        if not color:
            color = response.css(
                'ul.color span.swatchanchor::attr(data-variation-values)').extract_first()
        color_json = json.loads(color)

        color = color_json['attributeValue']

        for counter in range(4):
            image_url = "{}{}_{}_xl".format(self.images_domain, product['retailer_sku'] , color )
            if counter != 0:
                image_url = image_url + "_" + str(counter)
            counter += 1
            product['image_urls'].append(image_url)

        for size in sizes:
            product_sku = ProductSku()
            product_sku['color'] = color
            product_sku['currency'] = product['currency']
            product_sku['original_price'] = response.css(
                'span.price-standard::text').extract_first()
            product_sku['discounted_price'] = response.css(
                'span.price-sales::attr(content)').extract_first()
            size = size.strip('\n')
            product_sku['size'] = size
            product['skus'][color + '_' + size] = dict(product_sku)

        if last_color_flag:
            return product
