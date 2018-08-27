# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from enamora.items import EnamoraItem


class EnamoraSpider(CrawlSpider):
    """
    Crawl spider to scrap `www.enamora.com`
    """
    name = 'enamora'
    allowed_domains = ['www.enamora.de']
    start_urls = ['https://www.enamora.de/']

    rules = (
        Rule(LinkExtractor(allow=('damen/', 'herren/'), deny=('/meine-groesse', )), callback='parse'),
    )

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
        item['name'] = self.extract_name(response)
        item['brand'] = self.extract_brand(response)
        item['image_urls'] = self.extract_image_urls(response)
        item['care'] = self.extract_care(response)
        item['description'] = self.extract_description(response)
        sizes_request = scrapy.Request(url=self.extract_sizes_url(response), callback=self.parse_sizes)
        sizes_request.meta['item'] = item
        sizes_request.meta['color'] = self.extract_color(response)
        sizes_request.meta['price'] = self.extract_price(response)
        yield sizes_request

    def parse_sizes(self, response):
        item = response.meta['item']
        color = response.meta['color']
        price = response.meta['price']
        skus = list()
        sizes_info = response.css("li")
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
        item['skus'] = skus
        yield item

    @staticmethod
    def extract_sizes_url(response):
        url = response.css("ul[id='product-sizeselect'] include::attr(src)").extract_first()
        return url.replace('mi.', 'www.')

    @staticmethod
    def extract_name(response):
        return response.url.split('/')[-1].replace('.html', '').replace('-', ' ')

    @staticmethod
    def extract_brand(response):
        return response.css("a.brand::text").extract_first()

    @staticmethod
    def extract_image_urls(response):
        return response.css("ol.carousel-indicators li img::attr(src)").extract()

    @staticmethod
    def extract_care(response):
        return response.css("ul[id='pflegehinweise'] img::attr(alt)").extract()

    @staticmethod
    def extract_color(response):
        return response.css("p.product-color strong::text").extract_first()

    @staticmethod
    def extract_price(response):
        regular_price = response.css("p.regular strong::text").extract_first()
        previous_prices = []
        if not regular_price:
            regular_price = response.css("p.special strong::text").extract_first()
            previous_prices = [response.css("p.old small::text").extract_first(default='').strip()[:-1]]
        return {
            'currnency': regular_price.strip()[-1],
            'price': regular_price.strip()[:-1],
            'previous_price': previous_prices
        }

    @staticmethod
    def extract_description(response):
        response = response.replace(
            body=response.body.replace(b'<br />', b'\n').replace(b'<br>', b'\n')
        )
        headings = response.css("div[id='produkt-details'] span.control-label::text").extract()
        descriptions = response.css("div[id='produkt-details'] span.information-value::text").extract()
        return ["{} {}".format(headings[index], description)
                for index, description in enumerate(descriptions)]
