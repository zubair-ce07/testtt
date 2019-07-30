from math import ceil
from urllib.parse import urlencode

from scrapy import Request
from scrapy.spiders import Spider
from woolrich.spiders.woolrich_parser import WoolrichParser


class WoolrichSpider(Spider):
    name = 'woolrichspider'
    SIZE_BACKLOG = 'size_backlog'
    COLOUR_BACKLOG = 'colour_backlog'
    TRAIL = 'trail'
    ITEM = 'item'

    start_urls = [
        'https://www.woolrich.eu/en/gb/home'
    ]

    def parse(self, response):
        for url in response.css('.marked a::attr(href)')[:-1].getall():
            yield Request(url=url, callback=self.parse_listing)

    def parse_listing(self, response):
        products_on_page, remaining_products = WoolrichParser.get_page_meta(response)
        requests_count = ceil(remaining_products / products_on_page)
        for index in range(0, requests_count):
            params = {
                'sz': products_on_page,
                'start': products_on_page * index
            }
            yield Request(url=f'{response.url}?{urlencode(params)}',
                          meta={self.TRAIL: WoolrichParser.add_trail(response)},
                          callback=self.parse_product_listing)

    def parse_product_listing(self, response):
        for url in response.css('a.thumb-link::attr(href)').getall():
            yield Request(url=url, callback=self.parse_product,
                          meta={self.TRAIL: WoolrichParser.add_trail(response)})

    def parse_product(self, response):
        item = WoolrichParser.init_item(response)
        colour_backlog = WoolrichParser.get_colour_backlog(response)
        yield Request(url=colour_backlog[0], meta={self.ITEM: item,
                                                   self.COLOUR_BACKLOG: colour_backlog,
                                                   self.SIZE_BACKLOG: []},
                      callback=self.parse_colour_sizes)

    def parse_colour_sizes(self, response):
        meta = response.meta
        colour_backlog, item, size_backlog = meta[self.COLOUR_BACKLOG], meta[self.ITEM], meta[self.SIZE_BACKLOG]
        size_backlog.extend(WoolrichParser.get_size_backlog(response))
        colour_backlog = colour_backlog[1:]
        if colour_backlog:
            yield Request(url=colour_backlog[0], meta={self.ITEM: item,
                                                       self.COLOUR_BACKLOG: colour_backlog,
                                                       self.SIZE_BACKLOG: size_backlog},
                          callback=self.parse_colour_sizes)
        else:
            yield Request(url=size_backlog[0][0], meta={self.ITEM: item,
                                                        self.SIZE_BACKLOG: size_backlog},
                          callback=self.parse_skus)

    def parse_skus(self, response):
        size_backlog, item = response.meta[self.SIZE_BACKLOG], response.meta[self.ITEM]
        skus = item.get('skus', [])
        sku_item = WoolrichParser.get_sku(response, {'size': size_backlog[0][1]})
        skus.append(sku_item)
        item['skus'] = skus
        item['image_urls'].extend(WoolrichParser.get_image_urls(response))
        size_backlog = size_backlog[1:]
        if size_backlog:
            yield Request(url=size_backlog[0][0], meta={self.ITEM: item,
                                                        self.SIZE_BACKLOG: size_backlog},
                          callback=self.parse_skus)
        else:
            item['image_urls'] = set(item['image_urls'])
            yield item
