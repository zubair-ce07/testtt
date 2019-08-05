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

    ITEM = 'item'
    REQUESTS = 'requests'

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
        item['name'] = self.get_name(response)
        item['care'] = self.get_care(response)
        item['gender'] = self.get_gender(response)
        item['trail'] = response.meta.get('trail', [])
        item['category'] = self.get_categories(response)
        item['image_urls'] = self.get_image_urls(response)
        item['retailer_sku'] = self.get_product_id(response)
        item['description'] = self.get_description(response)
        response.meta['requests'] = self.get_colour_requests(response)

        return self.next_request_or_item(item, response)

    def next_request_or_item(self, item, response):
        requests = response.meta['requests']
        if not requests:
            return item

        request = requests.pop(0)
        request.meta[self.ITEM], request.meta[self.REQUESTS] = item, requests

        return request

    def parse_colour_requests(self, response):
        item, requests = response.meta[self.ITEM], response.meta[self.REQUESTS]
        requests.extend(self.get_size_requests(response))
        response.meta[self.REQUESTS] = requests

        return self.next_request_or_item(item, response)

    def parse_skus(self, response):
        item, requests = response.meta[self.ITEM], response.meta[self.REQUESTS]

        skus = item.get('skus', [])
        skus.append(self.get_sku(response))

        item['skus'] = skus
        item['image_urls'].extend(self.get_image_urls(response))
        response.meta[self.REQUESTS] = requests

        return self.next_request_or_item(item, response)

    def get_name(self, response):
        return response.css('#product-content .product-name::text').get().strip()

    def get_size_requests(self, response):
        urls = response.css('.swatches.size .swatchanchor::attr(href)').getall()
        return [Request(url=url, callback=self.parse_skus) for url in urls]

    def get_colour_requests(self, response):
        urls = response.css('.swatches.color .swatchanchor::attr(href)').getall()
        return [Request(url=url, callback=self.parse_colour_requests) for url in urls]

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
