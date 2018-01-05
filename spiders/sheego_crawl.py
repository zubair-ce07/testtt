# -*- coding: utf-8 -*-
import urllib.parse

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import SheegoItem


class SheegoSpider(CrawlSpider):
    name = 'sheego'
    allowed_domains = ['www.sheego.de']
    start_urls = ['http://www.sheego.de/']
    base_url = 'https://www.sheego.de/index.php?'
    products_ids = []

    rules = (Rule(LinkExtractor(restrict_css="a.js-next")),
             Rule(LinkExtractor(restrict_css='a.product__top'), callback="parse_product"),)

    def parse_item(self, response):
        item = SheegoItem()
        item['retailer_sku'] = self.get_retailer_sku(response)
        if item['retailer_sku'] in self.products_ids:
            yield None
        else:
            self.products_ids.append(item['retailer_sku'])

        item['name'] = self.get_name(response)
        item['brand'] = self.get_brand(response)
        item['retailer_sku'] = self.get_retailer_sku(response)
        item['categories'] = self.get_categories(response)
        item['total_rating'] = 5
        item['rating'] = self.get_rating(response)
        item['description'] = self.get_description(response)
        item['details'] = self.get_details(response)
        item['care'] = self.get_care(response)
        item['materials'] = self.get_material(response)
        item['image_urls'] = self.get_image_urls(response)
        item['price'] = self.get_price(response)
        item['currency'] = self.get_currency(response)

        item['skus'] = {}
        colour_urls = []
        size_urls = []
        length_varselids = self.get_length_varselids(response)
        colour_varselids = self.get_colour_varselids(response)
        for colour_varselid in colour_varselids:
            query_parameters = {
                'anid': item['retailer_sku'],
                'cl': 'oxwarticledetails',
                'varselid[0]': colour_varselid,
            }
            if length_varselids:
                for length_varselid in length_varselids:
                    query_parameters['varselid[1]'] = length_varselid
                    colour_url = self.make_url(query_parameters)
                    colour_urls.append(colour_url)
            else:
                colour_url = self.make_url(query_parameters)
                colour_urls.append(colour_url)

        if colour_urls:
            request = scrapy.Request(url=colour_urls.pop(0),
                                     callback=self.parse_colours,
                                     meta={
                                         'item': item,
                                         'colour_urls': colour_urls,
                                         'size_urls': size_urls,
                                     })
            yield request
        else:
            yield item

    def parse_colours(self, response):
        item = response.meta['item']
        size_urls = response.meta['size_urls']
        url_parameters = urllib.parse.parse_qs(urllib.parse.urlparse(response.url).query)
        varselid_key = '2' if ('varselid[1]' in url_parameters) else '1'

        size_varselids = self.get_size_varselids(response)
        for size_varselid in size_varselids:
            query_parameters = {'varselid[{0}]'.format(varselid_key): size_varselid}
            query_string = urllib.parse.urlencode(query_parameters)
            size_url = response.url + '&' + query_string
            size_urls.append(size_url)
        colour_urls = response.meta['colour_urls']
        if colour_urls:
            yield scrapy.Request(url=colour_urls.pop(0),
                                 callback=self.parse_colours,
                                 meta={
                                     'item': item,
                                     'colour_urls': colour_urls,
                                     'size_urls': size_urls,
                                 })
        else:
            yield scrapy.Request(url=size_urls.pop(0),
                                 callback=self.parse_sizes,
                                 meta={
                                     'item': item,
                                     'size_urls': size_urls,
                                 })

    def parse_sizes(self, response):
        item = response.meta['item']
        price = self.get_price(response)
        currency = self.get_currency(response)
        width = self.get_width(response)
        length = self.get_length(response)
        size = length + '_' + width if length else width
        colour = self.get_colour(response)
        stock = self.get_stock(response)
        sku_key = (colour + '_' + size).replace(' ', '_')
        sku_data = {
            'price': price,
            'currency': currency,
            'size': size,
            'colour': colour,
            'out_of_stock': stock
        }
        current_sku = {
            sku_key: sku_data
        }
        item['skus'].update(current_sku)

        size_urls = response.meta['size_urls']
        if size_urls:
            yield scrapy.Request(url=size_urls.pop(0),
                                 callback=self.parse_sizes,
                                 meta=response.meta)
        else:
            yield item

    def make_url(self, query_parameters):
        query_string = urllib.parse.urlencode(query_parameters)
        colour_url = self.base_url + query_string
        return colour_url

    def get_length(self, response):
        length = response.css('select.at-size-type-box option[selected="selected"]::text').extract_first()
        if length:
            return length.strip()

    def get_length_varselids(self, response):
        return response.css(
            'select.at-size-type-box option::attr(value)').extract()

    def get_stock(self, response):
        return response.css('meta[itemprop="availability"]::attr(content)').extract_first()

    def get_colour(self, response):
        return response.css('span.at-dv-color::text').extract_first()

    def get_width(self, response):
        return response.css('select.at-size-box option[selected="selected"]::text').extract_first().strip()

    def get_size_varselids(self, response):
        return response.css('div.sizespots__item::attr(data-varselid)').extract()

    def get_colour_varselids(self, response):
        return response.css('span.colorspots__item::attr(data-varselid)').extract()

    def get_currency(self, response):
        return response.css('meta[itemprop="priceCurrency"]::attr(content)').extract_first()

    def get_price(self, response):
        return response.css('meta[itemprop="price"]::attr(content)').extract_first()

    def get_image_urls(self, response):
        return response.css('div.p-details__image a::attr(href)').extract()

    def get_care(self, response):
        return response.css('div.p-details__careSymbols template ::text').extract()

    def get_details(self, response):
        return response.css('div.at-dv-article-details li ::text').extract()

    def get_description(self, response):
        return response.css('div[itemprop="description"] p ::text').extract()

    def get_rating(self, response):
        return response.css('a.c-rating::attr(title)').extract_first()

    def get_categories(self, response):
        return response.css('input[name="currentCategory"]::attr(value)').extract_first()

    def get_retailer_sku(self, response):
        return response.css('span.js-artNr::text').extract_first().strip()[:6]

    def get_brand(self, response):
        return response.css('meta[itemprop="manufacturer"]::attr(content)').extract_first()

    def get_name(self, response):
        return response.css('h1[itemprop="name"]::text').extract_first().strip()

    def get_material(self, response):
        material_dict = {}
        table_rows = response.css('table.p-details__material tr')
        for table_row in table_rows:
            row_data = table_row.css('td')
            material_dict_key = row_data.css('span::text').extract_first().strip()
            material_dict_value = row_data[1].css('::text').extract_first().strip()
            if material_dict_key:
                material_dict[material_dict_key] = material_dict_value
        return material_dict
