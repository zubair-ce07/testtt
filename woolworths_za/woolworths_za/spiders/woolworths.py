# -*- coding: utf-8 -*-
import json
import re
import time
from scrapy.http.request.form import FormRequest
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import CrawlSpider
from woolworths_za.items import WoolworthsItem


class WoolworthsSpider(CrawlSpider):
    name = "woolworths"
    allowed_domains = ["woolworths.co.za"]
    start_urls = ['http://www.woolworths.co.za/']
    product_filter = ['/Gifts',
                      '/Beauty',
                      '/Homeware',
                      '/Food',
                      '/Essentials',
                     ]
    rules = [
        Rule(LinkExtractor(restrict_css=[
            'div.horizontal-menu-container',
            'ul.nav-list--main',
            'ol.pagination__pages',
        ])),
        Rule(LinkExtractor(restrict_css='a.product-card__details',
                           deny=product_filter),
             callback='parse_item'),
    ]

    def parse_item(self, response):
        garment = WoolworthsItem()
        garment['name'] = self.product_name(response)
        garment['brand'] = 'Cecil'
        garment['category'] = self.product_category(response)
        garment['retailer'] = 'cecil-de'
        garment['price'] = self.product_price(response)
        garment['currency'] = self.product_currency(response)
        garment['gender'] = self.product_gender(response)
        garment['image_urls'] = self.product_images(response)
        garment['description'] = self.product_description(response)
        garment['industry'] = None
        garment['market'] = 'DE'
        garment['url'] = response.url
        garment['url_original'] = response.url
        garment['retailer_sku'] = self.product_retailer_sku(response)
        garment['care'] = self.product_care(response)
        garment['date'] = int(time.time())
        garment['skus'] = {}
        checklist = self.get_sku_checklist(response)
        if checklist:
            return self.get_skus(garment, checklist)
        return garment

    def product_name(self, response):
        selector = 'meta[itemprop="name"]::attr(content)'
        return response.css(selector).extract_first()

    def product_category(self, response):
        selector = 'li.breadcrumb__crumb a::text'
        return response.css(selector).extract()

    def product_currency(self, response):
        selector = 'meta[itemprop="priceCurrency"]::attr(content)'
        return response.css(selector).extract_first()

    def product_description(self, response):
        selector = 'meta[itemprop="description"]::attr(content)'
        return response.css(selector).extract_first()

    def product_retailer_sku(self, response):
        selector = 'meta[itemprop="productId"]::attr(content)'
        return response.css(selector).extract_first()

    def product_color(self, response):
        selector = 'meta[itemprop="color"]::attr(content)'
        return response.css(selector).extract_first().strip()

    def get_sku_checklist(self, response):
        colors_elem = response.css('img.colour-swatch')
        sizes_elem = response.css('a.product-size')
        colors = list(map(lambda elem: {'title': elem.css('::attr(title)').extract_first(),
                                        'id': re.findall('changeMainProductColour\((\d+)',
                                                         elem.css('::attr(onclick)')
                                                         .extract_first())[0]
                                        }, colors_elem))

        sizes = list(map(lambda elem: {'title': elem.css('::text').extract_first(),
                                       'id': re.findall('changeMainProductSize\(\d+,(\d+)',
                                                        elem.css('::attr(onclick)').extract_first())[0]
                                       }, sizes_elem))
        return [(color, size) for color in colors for size in sizes]

    def get_skus(self, garment, checklist):
        color, size = checklist.pop()
        price_url = 'http://www.woolworths.co.za/store/fragments/product-common/ww/price.jsp'
        return FormRequest(url=price_url,
                           formdata={'productItemId': garment['retailer_sku'],
                                     'colourSKUId': color['id'],
                                     'sizeSKUId': size['id'],
                                     },
                           callback=self.parse_price,
                           meta={'garment': garment,
                                 'checklist': checklist,
                                 'color': color,
                                 'size': size,
                                 }
                           )

    def parse_price(self, response):
        checklist = response.meta['checklist']
        garment = response.meta['garment']
        color = response.meta['color']
        size = response.meta['size']
        price_css = 'span.price::text'
        price = int(response.css(price_css).re_first('[\d|\.]+').replace('.',''))
        currency = garment['currency']
        skus = garment['skus']
        sku_id = color['title'].replace(' ', '_') + '_' + size['title']
        skus[sku_id] = {
            'color': color['title'],
            'size': size['title'],
            'price': price,
            'currency': currency,
        }
        if checklist:
            return self.get_skus(garment, checklist)
        else:
            return garment

    def product_price(self, response):
        selector = 'meta[itemprop="price"]::attr(content)'
        return int(response.css(selector).extract_first().replace('.',''))

    def product_old_price(self, response):
        selector = 'span.price--original::text'
        return int(response.css(selector).re_first('[\d|\.]+').replace('.',''))

    def product_images(self, response):
        selector = 'a[data-gallery-full-size]::attr(data-gallery-full-size)'
        links = response.css(selector).extract()
        return list(map(lambda link: 'http://'+link.lstrip('/'), links))

    def is_sale(self, response):
        return response.css('span.price--discounted')

    def product_care(self, response):
        desc = self.product_description(response)
        return re.findall('\d+%.*$', desc)

    def product_gender(self, response):
        patterns = [
            ('men', '/Men'),
            ('women', '/Women'),
            ('boys', '/Boys'),
            ('girls', '/Girls'),
            ('unisex', '/Unisex'),
            ('unisex-kids', '/School-Uniform'),
        ]

        for gender_pattern in patterns:
            gender = gender_pattern[0]
            url_pattern = gender_pattern[1]
            if url_pattern in response.url:
                return gender
