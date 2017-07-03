from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractor import LinkExtractor
from ..items import JulesProduct
import time


class JulesSpider(CrawlSpider):
    name = 'jules'
    allowed_domains = ['jules.com']
    start_urls = [
        'http://www.jules.com/fr/l/collection'
    ]

    rules = [Rule(LinkExtractor(restrict_css='.viewall')),
             Rule(LinkExtractor(restrict_css='.tiles-container', deny=['(ajax)$']),
                  callback='parse_products')
             ]

    def get_colours(self, response):
        return response.css('.swatch-label::text').extract()

    def get_skus(self, response):
        return {self.get_reference(response): {'color': self.get_colours(response),
                                               'currency': 'GBP',
                                               'price': self.get_price(response),
                                               'size': self.get_sizes(response)
                                               }}

    def get_sizes(self, response):
        return response.css('.va-size .swatchanchor::text').extract()

    def get_reference(self, response):
        return response.css('span[itemprop="productID"]::text').extract_first().strip()

    def get_price(self, response):
        try:
            return response.css('.newPrice .currency-price::text').extract_first() + '.' + \
                   response.css('.newPrice .price-decimal::text').extract_first().strip()
        except TypeError:
            return response.css('.actualPrice .pricePlain::text').extract_first() + '.' + \
                   response.css('.actualPrice .price-decimal::text').extract_first().strip()

    def get_name(self, response):
        return response.css('.name::text').extract_first()

    def get_description(self, response):
        return response.css('.product-desc-long::text').extract()

    def get_image_urls(self, response):
        return response.css('.product-image-link::attr(href)').extract()

    def parse_products(self, response):
        output = JulesProduct()
        output['description'] = self.get_description(response)
        output['image_urls'] = self.get_image_urls(response)
        output['name'] = self.get_name(response)
        output['url'] = response.url
        output['skus'] = self.get_skus(response)
        output['gender'] = 'Men'
        output['brand'] = 'Jules'
        output['date'] = time.strftime("%H:%M:%S")
        return output
