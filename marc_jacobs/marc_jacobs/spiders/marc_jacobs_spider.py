import json
import re

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractor import LinkExtractor

from marc_jacobs.items import MarcJacobsItem


class MarcJacobsSpider(CrawlSpider):
    name = 'marc_jacobs'
    start_urls = [
        'https://www.marcjacobs.com/'
    ]
    rules = (Rule(LinkExtractor(restrict_css='#navigation li.mobile-hidden .menu-vertical li',
                                ), follow=True),
             Rule(LinkExtractor(restrict_css='.infinite-scroll-placeholder', tags=('div',),
                                attrs=('data-grid-url',)), follow=True),
             Rule(LinkExtractor(restrict_css='.product-page-link', tags=('div',), attrs=('data-href',)),
                  callback='parse_products', follow=True),)

    def parse_products(self, response):
        item = MarcJacobsItem()
        item['url'] = self.get_url(response)
        item['name'] = self.get_name(response)
        item['brand'] = self.get_brand(response)
        item['description'] = self.get_description(response)
        colours_url, product_colours = self.get_product_colours(response)

        if product_colours:
            return scrapy.Request(colours_url.pop(0), callback=self.parse_colours,
                                  meta={'item': item, 'product_colours': product_colours,
                                        'colours_url': colours_url})

    def parse_colours(self, response):
        item = response.meta.get('item')
        colours_url = response.meta.get('colours_url')
        product_colours = response.meta.get('product_colours')
        colour = product_colours.pop(0)
        skus = response.meta.setdefault('skus', [])
        images_json_url = response.meta.setdefault('images_json_url', [])
        previous_price = self.get_previous_price(response)
        currency, price = self.get_price_and_currency(response)
        sizes = self.get_sizes(response)
        if not sizes:
            sizes = ['-']
        for size in sizes:
            skus.append({'sku_id': '{}_{}'.format(colour, size),
                         'colour': colour,
                         'size': size,
                         'previous_price': previous_price,
                         'price': price,
                         'currency': currency})
        images_json_url.append({'colour': colour, 'json_url': self.get_json_url(response)})

        if product_colours:
            return scrapy.Request(
                colours_url.pop(0), callback=self.parse_colours,
                meta={'images_json_url': images_json_url, 'item': item, 'skus': skus,
                      'product_colours': product_colours, 'colours_url': colours_url})
        else:
            item['skus'] = skus
            image_json_url = images_json_url.pop(0)
            if images_json_url:
                return scrapy.Request(
                    image_json_url.get('json_url'), callback=self.parse_image_urls,
                    meta={'colour': image_json_url.get('colour'),
                          'item': item, 'images_json_url': images_json_url})

    def parse_image_urls(self, response):
        colour = response.meta.get('colour')
        item = response.meta.get('item')
        images_json_url = response.meta.get('images_json_url')
        images_url = response.meta.setdefault('images_url', [])

        colour_wise_images_urls = []
        images_json = json.loads(re.search(r'{.*}', response.text).group(0))
        for img_url in images_json['items']:
            colour_wise_images_urls.append(img_url['src'])
        images_url.append({colour: colour_wise_images_urls})

        if images_json_url:
            json_url = images_json_url.pop(0)
            return scrapy.Request(
                json_url.get('json_url'), callback=self.parse_image_urls,
                meta={'colour': json_url.get('colour'), 'images_url': images_url,
                      'item': item, 'images_json_url': images_json_url})
        else:
            item['images_url'] = images_url
            return item

    def get_name(self, response):
        return response.css('#name::attr(value)').extract_first()

    def get_brand(self, response):
        return response.css('#name::attr(value)').extract_first()

    def get_url(self, response):
        return response.url

    def get_description(self, response):
        description = response.css('.tabs-menu .tab-content::text').extract()
        return [desc.strip() for desc in description if desc.strip()]

    def get_product_colours(self, response):
        return response.css('.value .swatches .color-swatch a::attr(href)').extract(), \
               response.css('.value .swatches .color-swatch a::text').extract()

    def get_previous_price(self, response):
        previous_price = response.css('#product-content .product-price span::text').extract_first()
        if not previous_price:
            previous_price = '-'
        return previous_price.strip('\r\t\n')

    def get_price_and_currency(self, response):
        price_and_currency = response.css('#product-content span[itemprop="price"]::attr(content)') \
            .extract_first().split()
        return price_and_currency[0], price_and_currency[1]

    def get_sizes(self, response):
        sizes = response.css('#va-size option::text').extract()
        return [size.strip() for size in sizes[1:] if size.strip()]

    def get_json_url(self, response):
        return response.css('.product-images::attr(data-images)').extract_first()
