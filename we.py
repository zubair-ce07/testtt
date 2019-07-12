import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule


def clean(raw_data):
    raw_info = ''

    if isinstance(raw_data, list):
        for string in raw_data:
            if re.sub('\s+', '', string):
                raw_info += (re.sub('\s+', '', string))

        return raw_info

    if re.sub('\s+', '', raw_data):
        return re.sub('\s+', '', raw_data)


class WeItem(scrapy.Item):
    retailer_sku = scrapy.Field()
    gender = scrapy.Field()
    name = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()
    brand = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()
    requests = scrapy.Field()


class WeSpider(CrawlSpider):
    name = 'we'
    allowed_domains = ['wefashion.de']
    start_urls = [
        'https://www.wefashion.de/',
    ]

    rules = (
        Rule(LinkExtractor(restrict_css='.level-top-1')),
        Rule(LinkExtractor(restrict_css='.refinement-link ')),
        Rule(LinkExtractor(restrict_css='.name-link'), callback='parse'),
    )

    def parse(self, response):
        item = WeItem()

        item['retailer_sku'] = self.retailer_sku(response)
        item['gender'] = self.product_gender(response)
        item['name'] = self.product_name(response)
        item['category'] = self.product_category(response)
        item['url'] = self.product_url(response)
        item['brand'] = self.product_brand(response)
        item['description'] = self.product_description(response)
        item['care'] = self.product_care(response)
        item['image_urls'] = self.images_url(response)
        item['skus'] = {}
        item['requests'] = []

        color_queue = response.css('.emptyswatch ::attr(href)').getall()

        for color_url in color_queue:
            item['requests'].append(response.follow(color_url, callback=self.parse_sku))

        yield from self.request_or_yield(item)

    def retailer_sku(self, response):
        return response.css('.variation-select ::attr(data-product-id)').get()

    def product_gender(self, response):
        return response.css('[itemprop = "itemListElement"] span ::text')[1].get()

    def product_name(self, response):
        return response.css('li > .last ::text').get()

    def product_category(self, response):
        return response.css('[itemprop="itemListElement"] span ::text').getall()[1:]

    def product_url(self, response):
        return response.url

    def product_brand(self, response):
        return response.css('#productEcommerceObject ::attr(value)').re('\"brand\":\"(.+?)\"')[0]

    def product_description(self, response):
        return clean(response.css('[itemprop="description"] span ::text').getall())

    def product_care(self, response):
        return response.css('.washingInstructions ::text').get()

    def images_url(self, response):
        return response.css('.pdp-figure__image ::attr(data-image-replacement)').getall()

    def parse_sku(self, response):
        item = response.meta['item']
        color = clean(response.css('.variant-attribute--list.variant-attribute--color span ::text').get())
        price = response.css('.pdp-price .price-sales ::attr(data-price)').get()
        sizes = self.parse_size(response.css('.swatches .swatchanchor ::text ').getall())

        raw_sku = item['skus']

        for size in sizes:
            raw_sku.update({f'{color}_{size}': {
                'color': color,
                'price': price,
                'size': size
            }})

        item['skus'] = raw_sku
        yield from self.request_or_yield(item)

    def parse_size(self, raw_sizes):
        size = []
        for string in raw_sizes:
            if re.sub('\s+', '', string):
                size.append(re.sub('\s+', '', string))

        return size

    def request_or_yield(self, item):
        if item['requests']:
            request = item['requests'].pop()
            request.meta.update({'item': item})
            yield request
        else:
            item.pop('requests', None)
            yield item
