# -*- coding: utf-8 -*-
import scrapy
import datetime
from ..items import OrsayItemLoaderItem, OrsaySkuItem, ProductLoader
from scrapy.loader.processors import TakeFirst
from redis import Redis
from scutils.redis_queue import RedisQueue
import time


class OrsayProductsSpider(scrapy.Spider):
    name = 'orsay_products'
    allowed_domains = ['orsay.de',
                       'orsay.com']
    start_urls = ['http://www.orsay.com/de-de/']

    def parse(self, response):
        redis_conn = Redis()
        queue = RedisQueue(redis_conn, "item")

        while True:
            url = queue.pop()

            if url:
                yield response.follow(url, callback=self.parse_product)
            else:
                time.sleep(2)

    def parse_product(self, response):
        product = self.product_info(response)
        product_colors_link = response.css('#product_main ul.product-colors a[href^="http"]::attr(href)').get()

        if product_colors_link:
            yield response.follow(product_colors_link, callback=self.parse_product_color_skus,
                                  meta={'product': product})
        else:
            product['skus'] = self.product_color_skus(response)
            product['date'] = datetime.datetime.now()
            yield product

    def product_info(self, response):
        loader = ProductLoader(item=OrsayItemLoaderItem(), selector=response)
        loader.add_value("crawl_start_time", datetime.datetime.now())
        loader.add_css("name", "#product_main .product-name::text")
        loader.add_css("price", "#product_main .regular-price > .price::text")
        loader.add_css("description", ".product-info-and-care .description::text")
        loader.add_css("lang", "html[lang]::attr(lang)")
        loader.add_value("url", response.url)
        loader.add_css("brand", ".branding a[title]::attr(title)")
        loader.add_css("retailer_sk", "#product_main > .product-main-info > .sku::text", re='Artikel-Nr.: (.*)')
        loader.add_css("image_urls", ("#product_media > .product-image-gallery-thumbs"
                                       " > a[href]::attr(href)"))
        loader.add_css("care", (".product-info-and-care .product-care"
                                 " > .material::text"))
        loader.add_css("care",(".product-info-and-care .product-care "
                                " > .caresymbols img[src]::attr(src)"))
        loader.add_css("currency", "#product-options-wrapper .sizebox-wrapper::attr(data-currency)")
        loader.add_value("gender", "women")
        return loader.load_item()

    def parse_product_color_skus(self, response):
        product = response.meta['product']
        product['skus'] = self.product_color_skus(response)
        product['date'] = datetime.datetime.now()
        yield product

    def product_color_skus(self, response):
        product_color_info = {}

        load = ProductLoader(item=OrsaySkuItem(), selector=response)
        product_price = load.get_css("#product_main .regular-price > .price::text")
        product_currency_code = load.get_css("#product-options-wrapper .sizebox-wrapper::attr(data-currency)")
        product_id = load.get_css('#product_addtocart_form > .no-display > input[name="product"]::attr(value)',
                                  TakeFirst())
        product_color = load.get_css('#product_addtocart_form > .no-display > input[name="color"]::attr(value)')

        for size_detail in response.css('#product-options-wrapper .sizebox-wrapper > ul:first-child > li'):
            loader = ProductLoader(item=OrsaySkuItem(), selector=size_detail)
            product_size = loader.get_css("li::text", TakeFirst(), str.strip)
            loader.add_value("size", product_size)
            loader.add_value("price", product_price)
            loader.add_value("colour", product_color)
            loader.add_css("out_of_stock", 'li[data-qty = "0"]')
            loader.add_value("colour", product_color)
            loader.add_value("currency", product_currency_code)
            sku_item = loader.load_item()

            color_info_key = '{}_{}'.format(product_id, product_size)
            product_color_info[color_info_key] = sku_item
        return product_color_info