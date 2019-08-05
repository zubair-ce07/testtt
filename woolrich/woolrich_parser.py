import re

from scrapy import Request
from scrapy.spiders import Spider
from woolrich.items import WoolrichItem


class WoolrichParser(Spider):
    market = 'UK'
    currency = 'GBP'
    brand = 'woolrich'
    name = 'woolrichparser'
    retailer = 'woolrich-uk'

    SIZE_URLS = 'size_urls'
    COLOUR_URLS = 'colour_urls'
    ITEM = 'item'

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

    def parse(self, response):
        item = WoolrichItem()
        item['skus'] = []
        item['url'] = response.url
        item['market'] = self.market
        item['retailer'] = self.retailer
        item['trail'] = response.meta.get('trail', [])
        item['name'] = self.get_name(response)
        item['care'] = self.get_care(response)
        item['image_urls'] = self.get_image_urls(response)
        item['retailer_sku'] = self.get_product_id(response)
        item['gender'] = self.get_gender(response)
        item['description'] = self.get_description(response)
        item['category'] = self.get_categories(response)

        return self.make_colour_request(item, response)

    def make_colour_request(self, item, response):
        colour_urls = self.get_colour_urls(response)
        if colour_urls:
            params = {}
            params[self.ITEM] = item
            params[self.COLOUR_URLS] = colour_urls
            params[self.SIZE_URLS] = []
            return Request(url=colour_urls[0], meta=params, callback=self.parse_colour_requests)
        else:
            return item

    def parse_colour_requests(self, response):
        meta = response.meta
        colour_urls, item, size_urls = meta[self.COLOUR_URLS], meta[self.ITEM], meta[self.SIZE_URLS]
        size_urls.extend(self.get_size_urls(response))
        colour_urls = colour_urls[1:]

        params = {}
        params[self.ITEM] = item
        params[self.SIZE_URLS] = size_urls

        if colour_urls:
            params[self.COLOUR_URLS] = colour_urls
            yield Request(url=colour_urls[0], meta=params, callback=self.parse_colour_requests)
        else:
            yield Request(url=size_urls[0], meta=params, callback=self.parse_skus)

    def parse_skus(self, response):
        size_urls, item = response.meta[self.SIZE_URLS], response.meta[self.ITEM]

        skus = item.get('skus', [])
        skus_per_size = self.get_sku(response)
        skus.append(skus_per_size)

        item['skus'] = skus
        item['image_urls'].extend(self.get_image_urls(response))

        size_urls = size_urls[1:]
        if size_urls:
            params = {}
            params[self.ITEM] = item
            params[self.SIZE_URLS] = size_urls
            yield Request(url=size_urls[0], meta=params, callback=self.parse_skus)
        else:
            item['image_urls'] = set(item['image_urls'])
            yield item

    def get_name(self, response):
        return response.css('#product-content .product-name::text').get().strip()

    def get_size_urls(self, response):
        return response.css('.swatches.size .swatchanchor::attr(href)').getall()

    def get_colour_urls(self, response):
        return response.css('.swatches.color .swatchanchor::attr(href)').getall()

    def get_product_id(self, response):
        return response.css('input#pid::attr(value)').get()

    def get_categories(self, response):
        return response.css('.breadcrumb-element::text').getall()[:-1]

    def get_description(self, response):
        return self.sanitize_list(response.css('.description::text').getall())

    def get_care(self, response):
        return self.sanitize_list(response.css('.fit-content::text').getall())

    def get_size(self, response):
        return re.search(r'(?<=size\=).*(?=\&dwvar)', response.url).group(0)

    def get_image_urls(self, response):
        css = '#thumbnails .carousel-container-inner a::attr(href)'
        return response.css(css).getall()

    def get_gender(self, response):
        trail = [url for _, url in response.meta.get('trail') or []]
        genders_candidate = ' '.join([response.url] + trail).lower()

        for tag, gender in self.genders:
            if tag in genders_candidate:
                return gender

        return 'unisex-adults'

    def sanitize_price(self, price):
        return int(''.join(re.findall(r'\d+', price)))

    def sanitize_list(self, inputs):
        return [i.strip() for i in inputs]

    def get_sku(self, response):
        price_css = '#product-content .price-sales::text'
        colour_css = '.swatches.color .selected .swatch::text'

        sku_item = {}
        sku_item['currency'] = self.currency,
        sku_item['size'] = self.get_size(response)
        sku_item['colour'] = response.css(colour_css).get().strip()
        sku_item['price'] = self.sanitize_price(response.css(price_css).get())

        previous_prices = response.css('#product-content .price-standard::text').getall()
        if previous_prices:
            sku_item['previous_prices'] = [self.sanitize_price(p) for p in previous_prices]

        sku_item['sku_id'] = f'{sku_item["colour"].replace(" ", "-")}_{sku_item["size"]}'.lower()
        sku_item['in_stock'] = bool(response.css('.in-stock-msg::text').get())

        return sku_item
