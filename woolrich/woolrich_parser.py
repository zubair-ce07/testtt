from re import sub

from scrapy import Request
from scrapy.spiders import Spider
from woolrich.items import WoolrichItem


class WoolrichParser(Spider):
    market = 'UK'
    currency = 'GBP'
    brand = 'woolrich'
    name = 'woolrichparser'
    retailer = 'woolrich-uk'

    SIZE_BACKLOG = 'size_backlog'
    COLOUR_BACKLOG = 'colour_backlog'
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
        colour_backlog = self.get_colour_backlog(response)

        params = {}
        params[self.ITEM] = item
        params[self.COLOUR_BACKLOG] = colour_backlog
        params[self.SIZE_BACKLOG] = []

        return Request(url=colour_backlog[0], meta=params, callback=self.parse_colour_sizes)

    def parse_colour_sizes(self, response):
        meta = response.meta
        colour_backlog, item, size_backlog = meta[self.COLOUR_BACKLOG], meta[self.ITEM], meta[self.SIZE_BACKLOG]
        size_backlog.extend(self.get_size_backlog(response))
        colour_backlog = colour_backlog[1:]

        params = {}
        params[self.ITEM] = item
        params[self.SIZE_BACKLOG] = size_backlog

        if colour_backlog:
            params[self.COLOUR_BACKLOG] = colour_backlog
            yield Request(url=colour_backlog[0], meta=params, callback=self.parse_colour_sizes)
        else:
            yield Request(url=size_backlog[0][0], meta=params, callback=self.parse_skus)

    def parse_skus(self, response):
        size_backlog, item = response.meta[self.SIZE_BACKLOG], response.meta[self.ITEM]

        skus = item.get('skus', [])
        skus_per_size = self.get_sku(response, {'size': size_backlog[0][1]})
        skus.append(skus_per_size)

        item['skus'] = skus
        item['image_urls'].extend(self.get_image_urls(response))

        size_backlog = size_backlog[1:]
        if size_backlog:
            params = {}
            params[self.ITEM] = item
            params[self.SIZE_BACKLOG] = size_backlog
            yield Request(url=size_backlog[0][0], meta=params, callback=self.parse_skus)
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

    def get_size_backlog(self, response):
        css = '.swatches.size .swatchanchor::{}'
        sizes = [s.strip() for s in response.css(css.format('text')).getall()]
        urls = response.css(css.format('attr(href)')).getall()
        return list(zip(urls, sizes))

    def get_colour_backlog(self, response):
        return response.css('.swatches.color .swatchanchor::attr(href)').getall()

    def get_product_id(self, response):
        product_id = sub(r'.*dwvar_', '', response.url)
        return sub(r'_color.*', '', product_id)

    def get_categories(self, response):
        return response.css('.breadcrumb-element::text').getall()[:-1]

    def get_description(self, response):
        descriptions = response.css('.description::text').getall()
        return [description.strip() for description in descriptions]

    def get_care(self, response):
        return [care.strip() for care in response.css('.fit-content::text').getall()]

    def get_image_urls(self, response):
        css = '#thumbnails .carousel-container-inner a::attr(href)'
        return response.css(css).getall()

    def get_gender(self, response):
        genders_candidate = ' '.join([response.url]
                                     + [url for title, url in response.meta['trail']]
                                     ).lower()
        for tag, gender in self.genders:
            if tag in genders_candidate:
                return gender
        return 'unisex-adults'

    def get_sku(self, response, additional_attrs):
        colour_css = '.swatches.color .selected .swatch::text'
        price_css = '#product-content .price-sales::text'
        sku_item = additional_attrs
        sku_item['currency'] = self.currency,
        sku_item['colour'] = response.css(colour_css).get().strip()
        sku_item['price'] = int(response.css(price_css).get()[1:].replace('.', ''))

        previous_prices = response.css('#product-content .price-sales::text').getall()
        if previous_prices:
            previous_prices = [int(p[1:].replace('.', '')) for p in previous_prices]
            sku_item['previous_prices'] = previous_prices

        sku_item['sku_id'] = f'{sku_item["colour"].replace(" ", "-")}_{sku_item["size"]}'.lower()
        sku_item['in_stock'] = self.get_in_stock(response)
        return sku_item
