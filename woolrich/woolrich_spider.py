from math import ceil
from re import sub
from urllib.parse import urlencode

from scrapy import Request
from scrapy.spiders import Spider
from woolrich.items import WoolrichItem


class WoolrichSpider(Spider):
    market = 'UK'
    currency = 'GBP'
    brand = 'woolrich'
    name = 'woolrichspider'
    retailer = 'woolrich-uk'

    genders = [
        ('women', 'women'),
        ('female', 'women'),
        ('lady', 'women'),
        ('woman', 'women'),
        ('man', 'men'),
        ('male', 'men'),
        ('men', 'men'),
        ('boy', 'boys'),
        ('boys', 'boys'),
        ('girl', 'girls'),
        ('girls', 'girls'),
        ('kids', 'unisex-kids'),
        ('adults', 'unisex-adults'),
    ]

    start_urls = [
        'https://www.woolrich.eu/en/gb/home'
    ]

    def parse(self, response):
        for url in response.css('.marked a::attr(href)')[:-1].getall():
            yield Request(url=url, callback=self.parse_listing)

    def parse_listing(self, response):
        css = '.search-result-content::attr({})'
        page_result = response.css(f'{css.format("data-pagesize")}, {css.format("data-searchcount")}').getall()
        products_on_page, remaining_products = list(map(int, page_result))
        number_of_requests = ceil(remaining_products/products_on_page)
        for index in range(0, number_of_requests):
            params = {
                'sz': products_on_page,
                'start': products_on_page*index
            }
            yield Request(url=f'{response.url}?{urlencode(params)}', meta={'trail': self.add_trail(response)},
                          callback=self.parse_product_listing)

    def parse_product_listing(self, response):
        for url in response.css('a.thumb-link::attr(href)').getall():
            yield Request(url=url, callback=self.parse_product, meta={'trail': self.add_trail(response)})

    def parse_product(self, response):
        item = WoolrichItem()
        item['url'] = response.url
        item['market'] = self.market
        item['retailer'] = self.retailer
        item['trail'] = response.meta['trail']
        item['name'] = self.get_name(response)
        item['care'] = self.get_care(response)
        item['image_urls'] = self.get_image_urls(response)
        item['retailer_sku'] = self.get_product_id(response)
        item['gender'] = self.get_gender(response)
        item['description'] = self.get_description(response)
        item['category'] = self.get_categories(response)

        color_backlog = self.get_color_backlog(response)
        yield Request(url=color_backlog[0], meta={'item': item, 'color_backlog': color_backlog,
                                                  'size_backlog': []},
                      callback=self.parse_color_sizes)

    def parse_color_sizes(self, response):
        meta = response.meta
        color_backlog, item = meta['color_backlog'], meta['item']
        size_backlog = meta['size_backlog']
        size_backlog.extend(self.get_size_backlog(response))
        color_backlog = color_backlog[1:]
        if color_backlog:
            yield Request(url=color_backlog[0], meta={'item': item, 'color_backlog': color_backlog,
                                                      'size_backlog': size_backlog},
                          callback=self.parse_color_sizes)
        else:
            yield Request(url=size_backlog[0][0], meta={'item': item, 'size_backlog': size_backlog},
                          callback=self.parse_skus)

    def parse_skus(self, response):
        size_backlog, item = response.meta['size_backlog'], response.meta['item']
        skus = item['skus'] if item.get('skus') else []
        sku_item = {
            'currency': self.currency,
            'color': response.css('.swatches.color .selected .swatch::text').get().strip(),
            'price': float(response.css('#product-content .price-sales::text').get()[1:]),
            'size': size_backlog[0][1]
        }

        previous_prices = response.css('#product-content .price-sales::text').getall()
        if previous_prices:
            previous_prices = [float(p[1:]) for p in previous_prices]
            sku_item['previous_prices'] = previous_prices

        sku_item['sku_id'] = self.get_product_id(response)
        sku_item['in_stock'] = self.get_in_stock(response)
        skus.append(sku_item)
        item['skus'] = skus
        item['image_urls'].extend(self.get_image_urls(response))
        size_backlog = size_backlog[1:]
        if size_backlog:
            yield Request(url=size_backlog[0][0], meta={'item': item, 'size_backlog': size_backlog},
                          callback=self.parse_skus)
        else:
            item['image_urls'] = set(item['image_urls'])
            yield item

    def add_trail(self, response):
        trail = (response.css('head title::text').get(), response.url)
        return [*response.meta['trail'], trail] if response.meta.get('trail') else [trail]

    def get_in_stock(self, response):
        in_stock = response.css('.in-stock-msg::text').get()
        return int(sub(r'\sitem\sleft', '', in_stock)) if in_stock else 0

    def get_name(self, response):
        return response.css('#product-content .product-name::text').get().strip()

    def get_size_backlog(self,response):
        css = '.swatches.size .swatchanchor::{}'
        sizes = [s.strip() for s in response.css(css.format('text')).getall()]
        urls = response.css(css.format('attr(href)')).getall()
        return list(zip(urls, sizes))

    def get_color_backlog(self, response):
        return response.css('.swatches.color .swatchanchor::attr(href)').getall()

    def get_product_id(self, response):
        return response.css('.sku::attr(skuid)').get().strip()

    def get_categories(self, response):
        return response.css('.breadcrumb-element::text').getall()[:-1]

    def get_description(self, response):
        descriptions = response.css('.description::text').getall()
        return [description.strip() for description in descriptions]

    def get_care(self, response):
        return [care.strip() for care in response.css('.fit-content::text').getall()]
    
    def get_image_urls(self, response):
        return response.css('#thumbnails .carousel-container-inner a::attr(href)').getall()

    def get_gender(self, response):
        genders_candidate = ' '.join([response.url]
                                     + [url for title, url in response.meta['trail']]
                                     ).lower()
        for tag, gender in self.genders:
            if tag in genders_candidate:
                return gender
        return 'unisex-adults'
