# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
import datetime


class OrsaySpiderSpider(CrawlSpider):
    name = 'orsay_spider'
    allowed_domains = ['orsay.de',
                       'orsay.com']
    start_urls = ['http://www.orsay.com/de-de/']

    rules = (
                Rule(LinkExtractor(restrict_css=
                                   '#nav > .level0 > .level0 > .level1'),
                     follow=True),
                Rule(LinkExtractor(restrict_css=
                                   '.toolbar-top ul.pagination .next.i-next'),
                      follow=True),
                Rule(LinkExtractor(restrict_css=
                                   '#products-list > .item .product-image-wrapper'),
                     callback='parse_product', follow=True),
            )

    def parse_product(self, response):
        product_info = self.product_info(response)
        product_colors_links = response.css('#product_main ul.product-colors a[href^="http"]::attr(href)').getall()

        if product_colors_links:
            url = product_colors_links.pop()
            yield response.follow(url, callback=self.parse_product_color_skus,
                                  meta={'product': product_info, 'product_colors_links': product_colors_links})
        else:
            product_info['skus'] = self.product_color_skus(response)
            product_info['date'] = datetime.datetime.now()
            yield product_info

    def product_info(self, response):
        product = {
            'crawl_start_time': datetime.datetime.now(),
            'name': self.get_product_name(response),
            'price': self.get_product_price(response),
            'description': self.get_product_description(response),
            'lang': self.get_product_language(response),
            'url': self.get_product_link(response),
            'brand': self.get_product_brand(response),
            'retailer_sk': self.get_article_code(response),
            'image_urls': self.get_product_images(response),
            'care': self.get_product_care_info(response),
            'currency': self.get_product_currency(response),
            'gender': 'women',
            'skus' : {}
        }

        return product

    def get_product_currency(self, response):
        currency = response.css('#product-options-wrapper .sizebox-wrapper::attr(data-currency)').get()
        if currency == '\u20ac':
            currency = "EUR"
        else:
            currency = None
        return currency

    def get_product_care_info(self, response):
        return response.css('.product-info-and-care .product-care > .material::text').getall() + \
               response.css('.product-info-and-care .product-care > .caresymbols'
                            ' img[src]::attr(src)').getall()

    def get_product_images(self, response):
        return response.css('#product_media > .product-image-gallery-thumbs'
                            ' > a[href]::attr(href)').getall()

    def get_article_code(self, response):
        return response.css('#product_main > .product-main-info > .sku::text').get()

    def get_product_brand(self, response):
        return response.css('.branding a[title]::attr(title)').get()

    def get_product_link(self, response):
        return response.url

    def get_product_language(self, response):
        return response.css('html[lang]::attr(lang)').get()

    def get_product_description(self, response):
        return response.css('.product-info-and-care .description::text').getall()

    def get_product_price(self, response):
        return response.css('#product_main .regular-price > .price::text').get()

    def get_product_name(self, response):
        return response.css('#product_main .product-name::text').get()

    def get_product_stock_status(self, response):
        return True if response.css('li[data-qty = "0"]').get() else False

    def get_product_size(self, response):
        return response.css('li::text').get().strip()

    def get_product_color(self, response):
        return response.css('#product_addtocart_form > .no-display > input[name="color"]::attr(value)').get()

    def get_product_id(self, response):
        return response.css('#product_addtocart_form > .no-display > input[name="product"]::attr(value)').get()

    def parse_product_color_skus(self, response):
        product = response.meta['product']
        product_colors_links = response.meta['product_colors_links']
        product['skus'].update(self.product_color_skus(response))

        if product_colors_links:
            url = product_colors_links.pop()
            yield response.follow(url, callback=self.parse_product_color_skus,
                                  meta={'product': product, 'product_colors_links': product_colors_links})
        else:
            product['date'] = datetime.datetime.now()
            yield product

    def product_color_skus(self, response):
        product_color_info = {}
        product_id = self.get_product_id(response)
        product_color = self.get_product_color(response)
        product_price = self.get_product_price(response)
        product_currency_code = self.get_product_currency(response)

        for size_detail in response.css('#product-options-wrapper .sizebox-wrapper > ul:first-child > li'):
            product_size = self.get_product_size(size_detail)
            color_info = {
                'price': product_price,
                'colour': product_color,
                'out_of_stock': self.get_product_stock_status(size_detail),
                'size': product_size,
                'currency': product_currency_code
            }
            color_info_key = '{}_{}'.format(product_id, product_size)
            product_color_info[color_info_key] = color_info
        return product_color_info
