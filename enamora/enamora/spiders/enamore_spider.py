# -*- coding: utf-8 -*-
import requests
from scrapy.spiders import CrawlSpider
from scrapy.http import TextResponse

from enamora.items import EnamoraItem


class WhistlesSpider(CrawlSpider):
    """
    Crawl spider to scrap `www.whistles.com`
    """
    name = 'enamora'
    allowed_domains = ['www.enamora.de']
    start_urls = ['https://www.enamora.de/tommy-hilfiger-holiday-gift-giving-pyjama-navy-blazerscooter.html']

    def parse(self, response):
        items_pages = response.css("ul.nav.row li a::attr(href)")
        items_pages.append(response.css("a.btn.next::attr(href)").extract_first())
        for href in items_pages:
            yield response.follow(href, callback=self.parse, cookies={'locale': 'en'})

        for href in response.css("div.product > a::attr(href)"):
            yield response.follow(href, callback=self.parse_item)

    def parse_item(self, response):
        item = EnamoraItem()
        item['url'] = response.url
        item['name'] = self.get_name(response)
        item['brand'] = self.get_brand(response)
        item['image_urls'] = self.get_image_urls(response)
        item['care'] = self.get_care(response)
        item['description'] =  self.get_description(response)
        item['skus'] = self.get_skus(response)
        yield item

    @staticmethod
    def get_name(response):
        return response.css("h1[class*='product-name']::text").extract_first()

    @staticmethod
    def get_brand(response):
        return response.css("a.brand::text").extract_first()

    @staticmethod
    def get_image_urls(response):
        return response.css("ol.carousel-indicators li img::attr(src)").extract()

    @staticmethod
    def get_care(response):
        return response.css("ul[id='pflegehinweise'] img::attr(alt)").extract()

    @staticmethod
    def get_color(response):
        return response.css("p.product-color strong::text").extract_first()

    @staticmethod
    def get_price(response):
        sale_price = response.css("p.special strong::text").extract_first()
        if isinstance(sale_price, str):
            regular_price = response.css("p.special strong::text").extract_first(default='').strip()
            return {
                'unit': regular_price[-1].strip(),
                'price': sale_price.strip()[:-1].strip(),
                'previous_price': [regular_price[:-1].strip()]
            }
        regular_price = response.css("p.regular strong::text").extract_first(default='').strip()
        return {
            'unit': regular_price[-1].strip(),
            'price': regular_price[:-1].strip(),
            'previous_price': []
        }

    @staticmethod
    def get_description(response):
        heading = response.css("div[id='produkt-details'] span.control-label::text").extract()
        description = response.css("div[id='produkt-details'] span.information-value::text").extract()
        return ['{} {}'.format(h.strip(), d.strip()) for h, d in zip(heading, description)]

    @classmethod
    def get_skus(cls, response):
        color = cls.get_color(response)
        price = cls.get_price(response)
        skus = list()
        from pdb import set_trace; set_trace()
        sizes_request_url = response.css("ul[id='product-sizeselect'] include::attr(src)").extract_first()

        sizes_response = requests.get(url=sizes_request_url.replace('mi.', 'www.'))
        sizes_response = TextResponse(body=sizes_response.content, url=sizes_request_url.replace('mi.', 'www.'))
        sizes_info = sizes_response.css("li")
        for size_info in sizes_info:
            size = size_info.css("span::text").extract_first()
            sku = {
                'color': color,
                'size': size,
                'sku_id': "{}_{}".format(color.replace(' ', '_'), size)
            }
            if size_info.css("a[disabled*='disabled']"):
                sku['out_of_stock'] = True
            sku.update(price)
            skus.append(sku)
        return skus
