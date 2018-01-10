# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader.processors import TakeFirst

from ..items import OrsayProduct, ProductLoader


class OrsaySpider(scrapy.Spider):
    name = 'orsay_crawl'
    allowed_domains = ['orsay.com']
    start_urls = ['http://www.orsay.com/de-de/jerseytop-mit-spitze-10800698.html/']

    def parse(self, response):
        product = OrsayProduct()
        item_loader = ProductLoader(item=product, response=response)
        item_loader.add_css('lang', 'html::attr(lang)')
        item_loader.add_css('price', 'span.price::text')
        item_loader.add_css('currency', 'div.sizebox-wrapper::attr(data-currency)')
        item_loader.add_css('retailer_sku', 'input[name="sku"]::attr(value)')
        item_loader.add_css('name', 'h1.product-name::text')
        item_loader.add_css('description', 'p.description::text')
        item_loader.add_css('img_urls', 'div.product-image-gallery-thumbs > a::attr(href)')
        item_loader.add_css('material', 'p.material::text')
        item_loader.add_css('care', 'ul.caresymbols > li > img::attr(src)')
        item_loader.add_css('category', 'div.no-display > input[name="category_name"]::attr(value)')

        skus = self.get_skus(response, item_loader)
        item_loader.add_value('skus', skus)

        yield item_loader.load_item()

    def get_skus(self, response, item_loader):
        product_id = item_loader.get_css('input[name="sku"]::attr(value)', TakeFirst())
        price = item_loader.get_css('span.price::text', TakeFirst(), str.strip)
        currency = item_loader.get_css('div.sizebox-wrapper::attr(data-currency)', TakeFirst())
        colour = item_loader.get_css('div.no-display > input[name="color"]::attr(value)', TakeFirst())
        current_skus = {}
        size_selectors = response.css('div.sizebox-wrapper li.size-box')

        for size_selector in size_selectors:
            current_size = size_selector.css('::text').extract_first().strip()
            quantity = size_selector.css('::attr(data-qty)').extract_first()
            sku_value = {
                'currency': currency,
                'price': price,
                'size': current_size,
                'colour': colour,
                'out_of_stock': False if int(quantity) else True
            }
            sku_key = product_id + '_' + current_size
            current_skus[sku_key] = sku_value
        return current_skus

