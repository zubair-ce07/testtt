# -*- coding: utf-8 -*-
import scrapy
import datetime


class OrsaySpiderSpider(scrapy.Spider):
    name = 'orsay_spider'
    allowed_domains = ['orsay.de',
                       'orsay.com']
    start_urls = ['http://orsay.de/']

    def parse(self, response):
        product_categories = response.css('#nav > .level0')
        for category in product_categories:
            category_links = category.css('.level0 > .level1 > a[href]::attr(href)').get()
            if category_links:
                for link in category_links:
                    yield response.follow(link, self.parse_category)

    def parse_category(self, response):
        products_links = response.css('#products-list > .item .product-image-wrapper > a[href]::attr(href)').getall()
        for product_link in products_links:
            yield response.follow(product_link, self.parse_product)

        next_page = response.css('.toolbar-top ul.pagination .next.i-next::attr(href)').get()
        if next_page:
            yield scrapy.Request(next_page, self.parse_category)

    def parse_product(self, response):
        product_info = self.product_info(response)
        product_colors_links = response.css('#product_main ul.product-colors a[href^="http"]::attr(href)').getall()

        if product_colors_links:
            url = product_colors_links.pop()
            yield response.follow(url, callback=self.parse_product_color,
                                  meta={'product': product_info, 'product_colors_links': product_colors_links})
        else:
            color_info = self.product_color_info(response)
            product_info['skus'] = color_info
            product_info['date'] = datetime.datetime.now()
            yield product_info

    def product_info(self, response):
        currency = response.css('#product-options-wrapper .sizebox-wrapper::attr(data-currency)').get()

        if currency == '\u20ac':
            currency = "EUR"
        else:
            currency = None

        product = {
            'crawl_start_time': datetime.datetime.now(),
            'name': response.css('#product_main .product-name::text').get(),
            'price': response.css('#product_main .regular-price > .price::text').get(),
            'description': response.css('.product-info-and-care .description::text').getall(),
            'lang': response.css('html[lang]::attr(lang)').get(),
            'url': response.url,
            'brand': response.css('.branding a[title]::attr(title)').get(),
            'retailer_sk': response.css('#product_main > .product-main-info > .sku::text').get(),
            'image_urls': response.css('#product_media > .product-image-gallery-thumbs'
                                       ' > a[href]::attr(href)').getall(),
            'care': response.css('.product-info-and-care .product-care > .material::text').getall() + \
                    response.css('.product-info-and-care .product-care > .caresymbols'
                                 ' img[src]::attr(src)').getall(),
            'currency': currency,
            'gender': 'women',
        }

        return product

    def parse_product_color(self, response):
        product = response.meta['product']
        product_colors_links = response.meta['product_colors_links']
        color_info = self.product_color_info(response)

        if 'skus' in product:
            product['skus'].update(color_info)
        else:
            product['skus'] = color_info

        if product_colors_links:
            url = product_colors_links.pop()
            yield response.follow(url, callback=self.parse_product_color,
                                  meta={'product': product, 'product_colors_links': product_colors_links})
        else:
            product['date'] = datetime.datetime.now()
            yield product

    def product_color_info(self, response):
        product_color_info = {}
        product_id = response.css('#product_addtocart_form > .no-display > input[name="product"]::attr(value)').get()
        currency = response.css('#product-options-wrapper .sizebox-wrapper::attr(data-currency)').get()

        if currency == '\u20ac':
            currency = "EUR"
        else:
            currency = None

        for size_detail in response.css('#product-options-wrapper .sizebox-wrapper > ul:first-child > li'):
            out_of_stock = "False"
            product_out_of_stock = size_detail.css('li[data-qty = "0"]').get()
            if product_out_of_stock:
                out_of_stock = "True"

            product_size = size_detail.css('li::text').get().strip()
            color_info = {
                'price': response.css('#product_main .regular-price > .price::text').get(),
                'colour': response.css('#product_addtocart_form > .no-display > input[name="color"]::attr(value)').get(),
                'out_of_stock': out_of_stock,
                'size': product_size,
                'currency': currency
            }
            color_info_key = '{}_{}'.format(product_id, product_size)
            product_color_info[color_info_key] = color_info
        return product_color_info