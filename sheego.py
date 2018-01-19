# -*- coding: utf-8 -*-
import datetime
import re
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider


class SheegoSpider(CrawlSpider):
    name = 'sheego'
    allowed_domains = ['sheego.de']
    start_urls = ['https://www.sheego.de']
    color_link = 'https://www.sheego.de/index.php?anid={}&cl=oxwarticledetails&varselid%5B0%5D={}'
    size_link = 'https://www.sheego.de/index.php?anid={}&cl=oxwarticledetails&varselid%5B0%5D={}&' \
                'varselid%5B1%5D={}'
    length_link = 'https://www.sheego.de/index.php?anid={}&cl=oxwarticledetails&varselid%5B0%5D={}' \
                  '&varselid%5B1%5D={}&varselid%5B2%5D={}'

    rules = (
        Rule(LinkExtractor(restrict_css=
                           '.mainnav--top > .cj-mainnav__entry'),
             callback='parse_product', follow=True),
        Rule(LinkExtractor(restrict_css='.paging__btn > [rel="next"]'),
             follow=True),
        Rule(LinkExtractor(restrict_css=
                           '.pl__list > .js-product-box > a:first-child'),
             callback='parse_product', follow=True),
    )

    def parse_product(self, response):
        product = {
            'crawl_start_time': datetime.datetime.now(),
            'name': self.get_product_name(response),
            'retailer_sk': self.get_article_code(response),
            'price': self.get_product_price(response),
            'description': self.get_product_description(response),
            'lang': self.get_product_language(response),
            'url': self.get_product_link(response),
            'brand': self.get_product_brand(response),
            'image_urls': [],
            'care': self.get_product_care_info(response),
            'currency': self.get_product_currency(response),
            'gender': 'women',
            'skus': {},
        }

        skus_collection = []
        color_ids = self.get_product_color_ids(response)

        if color_ids:
            self.insert_color_requests(color_ids, product, skus_collection)
        else:
            product['skus'].update(self.get_product_info(response))

        if skus_collection:
            yield skus_collection.pop()
        else:
            yield product

    def parse_product_length(self, response):
        product = response.meta['product']
        skus_collection = response.meta['skus_collection']
        color = self.get_product_color(response)
        product['image_urls'] += self.get_product_images(response)
        product_lengths = self.get_product_length(response)

        if product_lengths:
            self.insert_length_requests(product_lengths, color, response)
        else:
            product_sizes = self.get_product_sizes(response)
            if product_sizes:
                self.insert_size_requests(product_sizes, color, response)

            else:
                out_of_stock = self.get_product_availability(response)
                product_skus = {
                    '{}_{}'.format(color, None) : self.get_product_info(response, color, out_of_stock = out_of_stock)
                }
                product['skus'].update(product_skus)

        if skus_collection:
            yield skus_collection.pop()
        else:
            yield product

    def parse_product_sizes(self, response):
        product = response.meta['product']
        skus_collection = response.meta['skus_collection']
        length = response.meta['length']
        color = response.meta['color']
        product_sizes = self.get_product_sizes(response)

        if product_sizes:
            self.insert_sku_requests(product_sizes, color, length, response)

        else:
            out_of_stock = self.get_product_availability(response)
            product_skus = {
                '{}_{}'.format(color, length) : self.get_product_info(response, color, length = length, out_of_stock = out_of_stock)
            }
            product['skus'].update(product_skus)

        if skus_collection:
            yield skus_collection.pop()
        else:
            yield product


    def get_product_sizes(self, response):
        return response.css('.js-variantSelector.size .sizespots__item::attr(data-varselid)').getall()

    def get_product_length(self, response):
        lengths = response.css('.js-groessentyp option::attr(value)').getall()
        return [length for length in lengths if length]

    def get_product_color_ids(self, response):
        return response.css('.colorspots__wrapper > .colorspots__item::attr(data-varselid)').getall()

    def get_product_currency(self, response):
        return response.css('[itemprop="priceCurrency"]::attr(content)').get()

    def get_product_care_info(self, response):
        care = response.css('.f-row > div:first-child table ::text').getall()
        return self.clean_data(care)

    def get_product_images(self, response):
        links = response.css('.p-details__image__thumb__container img::attr(data-src)').getall()
        return [link.split('?')[0] for link in links] #removes thumbnail part of url

    def get_article_code(self, response):
        product_code = response.css('.js-artNr::text').get()

        if product_code:
            results = re.search(r'([^\s]\d+)', product_code)
            return results.group(1)
        return product_code

    def get_product_brand(self, response):
        product_brand = response.css('.p-details__brand ::text').get()

        if product_brand:
            return product_brand.strip()
        return product_brand

    def get_product_link(self, response):
        return response.url

    def get_product_language(self, response):
        return response.css('html[lang]::attr(lang)').get()

    def get_product_description(self, response):
        description = response.css('#detailmore ::text').getall()
        return self.clean_data(description)

    def get_product_price(self, response):
        return response.css('.js-lastprice::attr(value)').get()

    def get_product_name(self, response):
        product_name = response.css('#js-details-info h1[itemprop="name"]::text').get()

        if product_name:
            search_results = re.search(r'^\s+(.*)', product_name)
            return search_results.group(1)
        return product_name

    def get_product_color(self, response):
        color = response.css('.p-details__variants .l-mb-5::text').getall()
        filtered_color = [c.strip(' \t\n\r') for c in color]
        return [c for c in filtered_color if c][0] #returns color after removing extra spaces

    def get_product_size(self, response):
        return response.css('.hidden.at-dv-size1::text').get()

    def product_skus(self, response):
        product = response.meta['product']
        skus_collection = response.meta['skus_collection']
        product_size = self.get_product_size(response)
        color = response.meta['color']
        length = response.meta['length']
        out_of_stock = self.get_product_availability(response)

        product_sku = {
            '{}_{}_{}'.format(color, length, product_size): self.get_product_info(response, color, product_size, length, out_of_stock)
        }
        product['skus'].update(product_sku)

        if skus_collection:
            yield skus_collection.pop()
        else:
            yield product

    def get_product_info(self, response, color = None, product_size = None, length = None, out_of_stock = True):
        product_info = {
            'price': self.get_product_price(response),
            'color': color,
            'currency': self.get_product_currency(response),
            'size': product_size,
            'length' : length,
            'out_of_stock' : out_of_stock,
        }
        return product_info

    def insert_size_requests(self, product_sizes, color, response, length = None):
        product = response.meta['product']
        color_id = response.meta['color_id']
        skus_collection = response.meta['skus_collection']

        for size in product_sizes:
            skus_collection.append(scrapy.Request(
                url=self.size_link.format(product['retailer_sk'], color_id, size),
                callback=self.product_skus,
                meta={
                    'product': product,
                    'color': color,
                    'length' : length,
                    'skus_collection': skus_collection
                }
            ))

    def insert_sku_requests(self, product_sizes, color, length, response):
        product = response.meta['product']
        color_id = response.meta['color_id']
        skus_collection = response.meta['skus_collection']

        for size in product_sizes:
            skus_collection.append(scrapy.Request(
                url=self.length_link.format(product['retailer_sk'], color_id, length, size),
                callback=self.product_skus,
                meta={
                    'product': product,
                    'color': color,
                    'length' : length,
                    'skus_collection': skus_collection
                }
            ))

    def insert_length_requests(self, product_lengths, color, response):
        product = response.meta['product']
        color_id = response.meta['color_id']
        skus_collection = response.meta['skus_collection']

        for length in product_lengths:
            skus_collection.append(scrapy.Request(
                url=self.size_link.format(product['retailer_sk'], color_id, length),
                callback=self.parse_product_sizes,
                meta={
                    'product': product,
                    'color': color,
                    'color_id' : color_id,
                    'length' : length,
                    'skus_collection': skus_collection
                }
            ))

    def insert_color_requests(self, color_ids, product, skus_collection):
        for color_id in color_ids:
            skus_collection.append(scrapy.Request(
                url=self.color_link.format(product['retailer_sk'], color_id),
                callback=self.parse_product_length,
                meta={
                    'product': product,
                    'color_id': color_id,
                    'skus_collection': skus_collection
                }
            ))

    def get_product_availability(self, response):
        availability = response.css('[itemprop="availability"]::attr(content)').get()

        if availability:
            return availability.split('/')[-1]
        return availability

    def clean_data(self, input):
        if type(input) is str:
            return re.sub(r'[\n\t\s]+', ' ', input)
        else:
            return [re.sub(r'[\n\t\s]+', ' ', i) for i in input]