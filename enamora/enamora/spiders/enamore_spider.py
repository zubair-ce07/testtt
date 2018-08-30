# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from enamora.items import EnamoraItem


class EnamoraSpider(CrawlSpider):
    """
    Crawl spider to scrap `www.enamora.com`
    """
    custom_settings = {
        'DOWNLOAD_DELAY': 0.1,
    }

    name = 'enamora'
    allowed_domains = ['www.enamora.de']
    start_urls = ['https://www.enamora.de/']

    rules = (
        Rule(LinkExtractor(
            restrict_css=("ul.nav.row li a", "a.btn.next"),
        ), callback='parse'),
        Rule(LinkExtractor(
            restrict_css=('div.product > a',)
        ), callback='parse_item'),
    )

    def parse_item(self, response):
        item = EnamoraItem()
        item['url'] = response.url
        item['name'] = self.extract_name(response)
        item['brand'] = self.extract_brand(response)
        item['image_urls'] = self.extract_image_urls(response)
        item['care'] = self.extract_care(response)
        item['description'] = self.extract_description(response)
        sizes_request = self.prepare_sizes_request(response)
        sizes_request.meta['item'] = item
        sizes_request.meta['color'] = self.extract_color(response)
        sizes_request.meta['price'] = self.extract_price(response)

        yield sizes_request

    def prepare_sizes_request(self, response):
        url = response.css(
            "ul[id='product-sizeselect'] include::attr(src)"
        ).extract_first().replace('mi.', 'www.')

        return scrapy.Request(url=url, callback=self.parse_sizes)

    @staticmethod
    def parse_sizes(response):
        item = response.meta['item']
        color = response.meta['color']
        price = response.meta['price']
        skus = list()
        raw_sizes = response.css("li")

        for raw_size_s in raw_sizes:
            size = raw_size_s.css("span::text").extract_first()
            sku = {
                'color': color,
                'size': size,
                'sku_id': "{}_{}".format(color, size)
            }

            if raw_size_s.css("a[disabled*='disabled']"):
                sku['out_of_stock'] = True
            sku.update(price)
            skus.append(sku)
        item['skus'] = skus

        yield item

    @staticmethod
    def extract_name(response):
        return response.css(
            "div.product h1 small::text"
        ).extract_first().replace('-', '')

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
        return response.css(
            "p.product-color strong::text"
        ).extract_first().replace(' ', '_')

    @staticmethod
    def extract_price(response):
        pricing = {}
        regular_price = response.css("p.regular strong::text").extract_first()

        if not regular_price:
            pricing['previous_prices'] = [
                response.css("p.old small::text").extract_first().strip().replace(',', '')
            ]
            regular_price = response.css("p.special strong::text").extract_first()

        pricing['price'] = regular_price[:-1].strip().replace(',', '')
        pricing['currency'] = regular_price.strip()[-1]

        return pricing

    @staticmethod
    def extract_description(response):
        response = response.replace(
            body=response.body.replace(b'<br />', b'\n').replace(b'<br>', b'\n')
        )
        description_area = response.css("div#produkt-details")
        descriptions = list()

        for description_entry in description_area:
            descriptions.append(
                "{} {}".format(
                    description_entry.css("span.control-label::text").extract_first().strip(),
                    description_entry.css("span.information-value::text").extract_first().strip()
                )
            )

        return descriptions
