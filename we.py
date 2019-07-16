import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


def clean(raw_data):
    if isinstance(raw_data, list):
        return [re.sub('\s+', ' ', data).strip() for data in raw_data
                if re.sub('\s+', ' ', data).strip()]
    elif isinstance(raw_data, str):
        return re.sub('\s+', ' ', raw_data).strip()


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

    listings_css = '.level-top-1'
    category_css = '.refinement-link'
    product_css = '.name-link'
    rules = (
        Rule(LinkExtractor(restrict_css=[listings_css,category_css]), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item'),
    )

    def parse_item(self, response):
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

        colour_urls = response.css('.emptyswatch ::attr(href)').getall()
        for color_url in colour_urls:
            item['requests'].append(response.follow(color_url, callback=self.parse_sku))

        yield from self.return_request_or_yield(item)

    def parse_sku(self, response):
        item = response.meta['item']
        color = clean(response.css('.variant-attribute--list.variant-attribute--color span ::text').get())
        price = response.css('.pdp-price .price-sales ::attr(data-price)').get()
        sizes = clean(response.css('.swatches .swatchanchor ::text ').getall())
        common_sku = {'color': color,
                      'price': price}

        for size in sizes:
            item['skus'].update({f'{color}_{size}': common_sku.update({'size': size})})
        yield from self.return_request_or_yield(item)

    def retailer_sku(self, response):
        return response.css('.variation-select ::attr(data-product-id)').get()

    def product_gender(self, response):
        return response.css('[itemprop = "itemListElement"] span ::text')[1].get()

    def product_name(self, response):
        return response.css('top-container > .last ::text').get()

    def product_category(self, response):
        return response.css('[itemprop="itemListElement"] span ::text').getall()[1:]

    def product_url(self, response):
        return response.url

    def product_brand(self, response):
        return response.css('#productEcommerceObject ::attr(value)').re_first('\"brand\":\"(.+?)\"')

    def product_description(self, response):
        return clean(response.css('[itemprop="description"] span ::text').getall())

    def product_care(self, response):
        return [response.css('.washingInstructions ::text').get()]

    def images_url(self, response):
        return response.css('.pdp-figure__image ::attr(data-image-replacement)').getall()

    def return_request_or_yield(self, item):
        if item['requests']:
            request = item['requests'].pop()
            request.meta.update({'item': item})
            yield request
        else:
            item.pop('requests', None)
            yield item

