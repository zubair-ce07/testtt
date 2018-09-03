# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from enamora.items import EnamoraItem


def clean_text(text):

    def clean(text_entry):
        return (text_entry.strip()
                .replace('_', '')
                .replace('-', '')
                .replace('<br>', '')
                .replace('<br />', '')
                .replace('\n', ' ')
                .raplace('\t', ' '))

    if text and isinstance(text, str):
        return clean(str)

    return [clean(text_entry) for text_entry in text]


def clean_price(price):
    return price.strip().replace('.', '').replace(',', '')


class EnamoraSpider(CrawlSpider):
    """
    Crawl spider to scrap `www.enamora.com`
    """
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
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
        sizes_request.meta['currency'] = self.extract_currency(response)

        yield sizes_request

    def prepare_sizes_request(self, response):
        css = response.css(
            "ul[id='product-sizeselect'] include::attr(src)"
        )
        url = css.extract_first().replace('mi.', 'www.')

        return scrapy.Request(url=url, callback=self.parse_sizes)

    def parse_sizes(self, response):
        item = response.meta['item']
        color = response.meta['color']
        currency = response.meta['currency']
        raw_sizes = response.css("li a")
        item['skus'] = self.prepare_skus(color, currency, raw_sizes)

        yield item

    @staticmethod
    def prepare_skus(color, currency, raw_sizes):
        skus = list()

        for raw_size_s in raw_sizes:
            sku = {
                'color': color,
                'size': raw_size_s.css("::attr(data-label)").extract_first(),
                'sku_id': raw_size_s.css("::attr(data-sku)").extract_first(),
                'price': clean_price(raw_size_s.css("::attr(data-price)").extract_first()),
                'currency': currency
            }
            availability_status = raw_size_s.css("::attr(data-qty)").extract_first()

            if not int(availability_status):
                sku['out_of_stock'] = True

            skus.append(sku)

        return skus

    @staticmethod
    def extract_name(response):
        css = response.css(
            "div.product h1 small::text"
        )
        return clean_text(css.extract_first())

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
        css = response.css(
            "p.product-color strong::text"
        )
        return css.extract_first().replace(' ', '_')

    @staticmethod
    def extract_currency(response):
        return response.css(
            "meta[property='og:price:currency']::attr(content)"
        ).extract_first()

    @staticmethod
    def extract_description(response):
        description_area = response.css("div#produkt-details")
        descriptions = list()

        for description_entry in description_area:
            descriptions.append(
                "{} {}".format(
                    ''.join(description_entry.css("span.control-label::text").extract()).strip(),
                    ''.join(description_entry.css("span.information-value::text").extract()).strip()
                )
            )

        return descriptions
