# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
import datetime
import re
import scrapy


class WoolWorthsSpider(CrawlSpider):
    name = 'woolworths'
    allowed_domains = ['woolworths.co.za']
    start_urls = ['http://www.woolworths.co.za']

    form_post_link = 'http://www.woolworths.co.za/store/fragments/product-common/ww/product-item.jsp'
    form_post_images_link = 'http://www.woolworths.co.za/store/fragments/product-common/ww/image-shots.jsp'
    post_price_link = 'http://www.woolworths.co.za/store/fragments/product-common/ww/price.jsp?' \
                      'productItemId={}&colourSKUId={}&sizeSKUId={}'
    rules = (
        Rule(LinkExtractor(restrict_css=
                           '#main-nav > .main-nav__list > .main-nav__list-item > .main-nav__list >'
                            '.main-nav__list-item > a:first-child'),
             follow=True),
        Rule(LinkExtractor(restrict_css='.pagination > a:last-child'),
             follow=True),
        Rule(LinkExtractor(restrict_css=
                           '.product-list__list > .grid > .product-list__item'),
             callback='parse_product', follow=True),
    )

    def parse_product(self, response):
        product_id = self.get_article_code(response)
        product = {
            'crawl_start_time': datetime.datetime.now(),
            'name': self.get_product_name(response),
            'retailer_sk': product_id,
            'price': self.get_product_price(product_id, response),
            'description': self.get_product_description(response),
            'lang': self.get_product_language(response),
            'url': self.get_product_link(response),
            'brand': self.get_product_brand(response),
            'image_urls': [],
            'care': self.get_product_care_info(response),
            'currency': self.get_product_currency(product_id, response),
            'gender': 'women',
            'skus': {},
        }

        skus_collection = []
        color_ids = self.get_product_color_ids(response)

        if color_ids:
            self.insert_color_requests(color_ids, product, skus_collection)
        else:
            product['skus'].update(self.get_product_info(response, product_id))

        if skus_collection:
            yield skus_collection.pop()
        else:
            yield product

    def parse_product_images(self, response):
        product = response.meta['product']
        skus_collection = response.meta['skus_collection']
        product['image_urls'] += self.get_product_images(response)

        if skus_collection:
            yield skus_collection.pop()
        else:
            yield product

    def parse_product_sizes(self, response):
        product = response.meta['product']
        color_id = response.meta['color_id']
        skus_collection = response.meta['skus_collection']
        color = self.get_product_color(color_id, response)
        product_sizes = self.get_product_sizes(response, color_id)

        if product_sizes:
            self.insert_size_requests(product_sizes, color, response)

        else:
            product_skus = {
                '{}_{}'.format(color_id, None) : self.get_product_info(response, product["retailer_sk"], color)
            }
            product['skus'].update(product_skus)

        if skus_collection:
            yield skus_collection.pop()
        else:
            yield product

    def get_product_sizes(self, response, color_id):
        return re.findall(r'changeMainProductSize\({},(.*?),'.format(color_id), str(response.body))

    def get_product_color_ids(self, response):
        return re.findall(r'changeMainProductColour\((.*?),', str(response.body))

    def get_product_currency(self, product_id, response):
        return response.css('#price_{} > span[itemprop="priceCurrency"]::attr(content)'.format(product_id)).get()

    def get_product_care_info(self, response):
        return response.css('.accordion__segment--chrome:nth-child(2) img::attr(src)').getall()

    def get_product_images(self, response):
        return response.css('div[data-js="pdp-carousel"] a::attr(href)').getall()

    def get_article_code(self, response):
        return response.css('.accordion__segment--chrome:first-child > .accordion__content--chrome >'
                            '.list--silent li:last-child::text').get()

    def get_product_brand(self, response):
        return response.css('.site-header__wrapper--logo > a::text').get()

    def get_product_link(self, response):
        return response.url

    def get_product_language(self, response):
        return response.css('html[lang]::attr(lang)').get()

    def get_product_description(self, response):
        return response.css('.accordion__segment--chrome:first-child ::text').getall()

    def get_product_price(self, product_id, response):
        return response.css('#price_{} > span[itemprop="price"]::text'.format(product_id)).get()

    def get_product_name(self, response):
        product_name = response.css('.product-detail__grid > h1:first-child::text').get()
        if product_name:
            return product_name.strip()
        else:
            return None

    def get_product_color(self, color_id, response):
        return response.css('.nav-list-x.nav-list-x--wrap > .nav-list-x__item >' \
                'img[onclick*="{}"]::attr(title)'.format(color_id)).get()

    def get_product_size(self, size, response):
        return response.css('.nav-list-x.product__size-selector a[onclick*="{}"]::text'.format(size)).get()

    def product_skus(self, response):
        product = response.meta['product']
        color_id = response.meta['color_id']
        size = response.meta['size']
        skus_collection = response.meta['skus_collection']
        size_text = response.meta['size_text']
        color = response.meta['color']

        skus_collection.append(scrapy.FormRequest(
            url=self.post_price_link.format(product['retailer_sk'], color_id, size),
            formdata={
                'productItemId': product['retailer_sk'],
                'colourSKUId': color_id,
                'sizeSKUId': size
            },
            callback=self.parse_product_sku,
            meta={
                'product': product,
                'skus_collection': skus_collection,
                'color': color,
                'color_id': color_id,
                'size_text': size_text,
            }
        ))

        if skus_collection:
            yield skus_collection.pop()
        else:
            yield product

    def parse_product_sku(self, response):
        product = response.meta['product']
        skus_collection = response.meta['skus_collection']
        color = response.meta['color']
        color_id = response.meta['color_id']
        product_size = response.meta['size_text']

        product_sku = {
            '{}_{}'.format(color_id, product_size) : self.get_product_info(response, product["retailer_sk"], color, product_size)
        }
        product['skus'].update(product_sku)

        if skus_collection:
            yield skus_collection.pop()
        else:
            yield product

    def get_product_info(self, response, product_id, color = None, product_size = None):
        product_info = {
            'price': self.get_product_price(product_id, response),
            'colour': color,
            'currency': self.get_product_currency(product_id, response),
            'size': product_size,
        }
        return product_info

    def insert_size_requests(self, product_sizes, color, response):
        product = response.meta['product']
        color_id = response.meta['color_id']
        skus_collection = response.meta['skus_collection']

        for size in product_sizes:
            skus_collection.append(scrapy.FormRequest(
                url=self.form_post_link,
                formdata={
                    'productItemId': product['retailer_sk'],
                    'colourSKUId': color_id,
                    'sizeSKUId': size
                },
                callback=self.product_skus,
                meta={
                    'product': product,
                    'color_id': color_id,
                    'color': color,
                    'size': size,
                    'size_text': self.get_product_size(size, response),
                    'skus_collection': skus_collection
                }
            ))

    def insert_color_requests(self, color_ids, product, skus_collection):
        for color_id in color_ids:
            skus_collection.append(scrapy.FormRequest(
                url=self.form_post_link,
                formdata={
                    'productItemId': product['retailer_sk'],
                    'colourSKUId': color_id
                },
                callback=self.parse_product_sizes,
                meta={
                    'product': product,
                    'color_id': color_id,
                    'skus_collection': skus_collection
                }
            ))
            skus_collection.append(scrapy.FormRequest(
                url=self.form_post_images_link,
                formdata={
                    'productId': product['retailer_sk'],
                    'colourSKUId' : color_id,
                    'productsPageType' : 'clothingProducts'
                },
                callback=self.parse_product_images,
                meta={
                    'product': product,
                    'skus_collection': skus_collection
                }
            ))