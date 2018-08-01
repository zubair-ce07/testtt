import json
import re

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class SheegoSpider(CrawlSpider):
    name = 'sheegocrawler'
    allowed_domains = ['sheego.de']
    start_urls = ['https://www.sheego.de']

    rules = (
        Rule(LinkExtractor(restrict_css=['.cj-mainnav__entry .cj-mainnav__entry-title',
                                         '.paging__btn.paging__btn--next .js-next'])),
        Rule(LinkExtractor(restrict_css='.js-product__wrapper .js-product__link'), callback='parse_products')
    )

    def parse_products(self, response):
        json_resp = self.extract_json_data(response)
        item = {
            'care': self.extract_care(response),
            'description': self.extract_description(response),
            'image_urls': self.extract_image_urls(response),
            'product_name': self.extract_product_name(json_resp),
            'sku': self.extract_sku_id(json_resp),
            'url': response.url,
            'skus': self.product_skus(response, json_resp)
        }

        color_links = self.extract_color_links(response)
        if color_links:
            yield Request(color_links.pop(0), callback=self.parse_colors,
                          meta={'color_links': color_links, 'item': item})
        else:
            yield item

    def parse_colors(self, response):
        color_links = response.meta['color_links']
        item = response.meta['item']
        json_resp = self.extract_json_data(response)
        item['image_urls'] += self.extract_image_urls(response)
        item['skus'].update(self.product_skus(response, json_resp))

        if color_links:
            yield Request(color_links.pop(0), callback=self.parse_colors,
                          meta={'color_links': color_links, 'item': item})
        else:
            yield item

    def product_skus(self, response, json_resp):
        skus = {}
        sku_id = self.extract_product_sku(json_resp)
        color = self.extract_color(response).encode('utf-8')
        for size, stock in self.extract_sizes_availability(response).items():
            values = {
                'price': self.extract_price(json_resp),
                'color': color,
                'size': size,
                'stock': stock
            }
            skus['{0}_{1}'.format(sku_id, size)] = values
        return skus

    def extract_json_data(self, response):
        return json.loads(response.css('.js-webtrends-data::attr(data-webtrends)').extract_first())

    def extract_color_links(self, response):
        colors = response.css('.cj-slider__slides script').extract_first().split(' = [')[1].split('];')[0].split(',')
        url = response.url.split('=')[0]
        prev_col = response.url.split('=')[1][1:-1]
        return ['{0}={1}'.format(url, col_link[1:-1]) for col_link in colors if prev_col not in col_link]

    def extract_color(self, response):
        return response.css('.p-details__variants.l-f-d-c .l-mb-5::text').extract()[1].strip()

    def extract_sizes_availability(self, response):
        sizes = response.css('.c-sizespots div::text').extract()
        sizes = [size.strip() for size in sizes]
        stock = response.css('.c-sizespots div::attr(class)').extract()
        stock = ['Not Available' if 'strike' in st else 'Available' for st in stock]
        return dict(zip(sizes, stock))

    def extract_image_urls(self, response):
        return response.css('.p-details__image__main .MagicZoom::attr(href)').extract()

    def extract_product_name(self, response):
        return response['productName']

    def extract_care(self, response):
        return self.clean_spaces(''.join(care for care in response.css(
            '.p-details__material.l-mb-10 td::text').extract()))

    def extract_description(self, response):
        return self.clean_spaces(', '.join(desc for desc in response.css(
            '.l-hidden-xs-s .l-list.l-list--nospace li::text').extract()))

    def extract_sku_id(self, response):
        return response['productId']

    def extract_product_sku(self, response):
        return response['productSku']

    def extract_price(self, response):
        return response['productPrice']

    def clean_spaces(self, string):
        return ''.join(re.sub("\s+", ' ', string))
