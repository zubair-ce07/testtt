# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import OrsayDeProduct


class OrsayLinksExtractorSpider(CrawlSpider):
    name = 'orsay_links_extractor'
    allowed_domains = ['orsay.com']
    start_urls = ['http://orsay.com/']

    rules = (
        Rule(LinkExtractor(restrict_css='ul#nav',), follow=True),
        Rule(LinkExtractor(restrict_css='a.next',), follow=True),
        Rule(LinkExtractor(restrict_css='a.product-image',), callback='parse_products',),
    )

    def parse_products(self, response):
        product = OrsayDeProduct()
        colors = response.css('ul.product-colors > li a::attr(href)').extract()
        colors.remove('#')
        product['skus'] = {}
        product['img_urls'] = []
        product['lang'] = response.css('html::attr(lang)').extract_first()
        product['price'] = response.css('span.price::text').extract_first().strip()
        product['currency'] = response.css('div.sizebox-wrapper::attr(data-currency)').extract_first()

        product['retailer_sku'] = response.css('input[name="sku"]::attr(value)').extract_first()[0:6]
        product['name'] = response.css('h1.product-name::text').extract_first()
        product['description'] = response.css('p.description::text').extract_first().strip()
        product['img_urls'].append(response.css('div.product-image-gallery-thumbs > a::attr(href)').extract())

        product['material'] = response.css('p.material::text').extract_first()
        product['care'] = response.css('ul.caresymbols > li > img::attr(src)').extract()
        product['category'] = response.css(
            'div.no-display > input[name="category_name"]::attr(value)').extract_first()

        self.create_skus(response, product)
        if colors:
            request = scrapy.Request(url=colors[0], callback=self.parse_colors)
            request.meta['item'] = product
            request.meta['colors'] = colors
            yield request
        else:
            yield product

    def parse_colors(self, response):
        if response.meta:
            product = response.meta['item']
            colors = response.meta['colors']
            colors.pop(0)

            product['img_urls'].append(response.css('div.product-image-gallery-thumbs > a::attr(href)').extract())
            self.create_skus(response, product)
            if colors:
                request = scrapy.Request(url=colors[0], callback=self.parse_colors)
                request.meta['item'] = product
                request.meta['colors'] = colors
                yield request
            else:
                yield product

    def create_skus(self, response, product):
        product_id = response.css('input[name="sku"]::attr(value)').extract_first()

        price = response.css('span.price::text').extract_first().strip()
        currency = response.css('div.sizebox-wrapper::attr(data-currency)').extract_first()

        sizes = response.css('div.sizebox-wrapper li.size-box')
        color = response.css('div.no-display > input[name="color"]::attr(value)').extract_first()

        for size in sizes:
            current_size = size.css('::text').extract_first().strip()
            quantity = size.css('::attr(data-qty)').extract_first()
            sku_data = {
                'currency': currency,
                'price': price,
                'size': current_size,
                'color': color,
                'out_of_stock': False if int(quantity) else True
            }
            key = product_id + '_' + current_size
            product['skus'][key] = sku_data
