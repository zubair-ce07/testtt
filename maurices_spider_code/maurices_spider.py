# -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from maurices.items import MauricesProduct


class MauricesSpider(CrawlSpider):
    name = 'maurices_spider'
    allowed_domains = ['maurices.com']
    start_urls = ['https://www.maurices.com']
    product_page_url = 'https://www.maurices.com/maurices/plp/includes/plp-filters.jsp?'
    product_skus_url = 'https://www.maurices.com/maurices/baseAjaxServlet?pageId=PDPGetProduct&Action=PDP.getProduct&id='

    rules = (
        Rule(LinkExtractor(allow=(r'/c/.*'), restrict_css=('.menu'))),
        Rule(LinkExtractor(allow=(r'/p/.*N-[0-9]*$'), restrict_css=('.nav')),
             callback='parse_product_subcatagory')
    )

    def parse_product_subcatagory(self, response):
        product_urls = response.meta.get('product_urls')
        if product_urls is None:
            sub_catagory_id = response.url.split('/')[-1].replace('-', '=')
            url = self.product_page_url + sub_catagory_id + '&No=0'
            yield scrapy.Request(url, callback=self.parse_product_subcatagory, meta={'product_urls': list()})
        else:
            html_resp = json.loads(response.body).get(
                'product_grid').get('html_content')
            product_urls.extend(Selector(text=html_resp).css(
                '.mar-prd-item-image-container::attr(href)').extract())
            next_page_url = json.loads(response.body).get('nextPageUrl')
            if next_page_url:
                url = response.url
                url = url[:url.find('No=')+3] + re.search('No=(.+?)&',
                                                          next_page_url).group(1)
                yield scrapy.Request(url, callback=self.parse_product_subcatagory, meta={'product_urls': product_urls})
            else:
                for product_url in product_urls:
                    product_url = 'https://www.maurices.com' + product_url
                    yield scrapy.Request(product_url, callback=self.parse_product)

    def parse_product(self, response):
        product = MauricesProduct()
        product['brand'] = 'maurices'
        product['name'] = response.css(
            '.mar-product-title::text').extract_first()
        product['description'] = response.css(
            '.mar-product-description-content li::text').extract()
        product['retailer_sku'] = response.url.split('/')[-1]
        product['image_urls'] = list()
        product['url'] = response.url
        product['skus'] = dict()
        url = self.product_skus_url + response.url.split('/')[-1]
        yield scrapy.Request(url, callback=self.find_and_append_skus, meta={'product': product})

    def find_and_append_skus(self, response):
        product = response.meta.get('product')
        product_detail = json.loads(response.body)['product'][0]
        for color in product_detail['all_available_colors'][0]['values']:
            product['image_urls'].append(color['sku_image'])
        colors = self.get_attributes(
            product_detail['all_available_colors'])
        sizes = self.get_attributes(
            product_detail['all_available_sizes'])
        self.add_skus(product, product_detail, colors, sizes)
        self.update_skus(product, product_detail, colors, sizes)
        yield product

    def get_attributes(self, attribute_list):
        attributes = dict()
        if attribute_list:
            for attribute in attribute_list[0]['values']:
                attributes[str(attribute['id'])] = attribute['value']
        return attributes

    def add_skus(self, product, product_detail, colors, sizes):
        product['category'] = product_detail['ensightenData'][0]['categoryPath']
        for sku in product_detail['skus']:
            color_id = sku['color']
            size_id = sku['size']
            key = str(colors[color_id] + '_' + sizes[size_id])
            product['skus'][key] = {
                'color': colors[color_id],
                'currency': 'USD',
                'price': product_detail['all_available_colors'][0]['values'][0]['prices']['sale_price'],
                'size': sizes[size_id],
            }

    def update_skus(self, product, product_detail, colors, sizes):
        for color_id, size_id in zip(colors, sizes):
            key = str(colors[color_id] + '_' + sizes[size_id])
            if not product['skus'].get(key):
                product['skus'][key] = {
                    'color': colors[color_id],
                    'currency': 'USD',
                    'price': product_detail['all_available_colors'][0]['values'][0]['prices']['sale_price'],
                    'size': sizes[size_id],
                    'out_of_stock': True
                }
