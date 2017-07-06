from scrapy.spiders import CrawlSpider, Rule, Request
from scrapy.linkextractor import LinkExtractor
from ..items import JulesProduct
import time


class JulesSpider(CrawlSpider):
    name = 'jule'
    allowed_domains = ['jules.com']
    start_urls = [
        'http://www.jules.com/fr/p/polo-boutonne-708690.html?&dwvar_708690_color=9010'
    ]

    # rules = [Rule(LinkExtractor(restrict_css='.viewall')),
    #          Rule(LinkExtractor(restrict_css='.tiles-container', deny=['(ajax)$']),
    #               callback='parse_products'
    #               )
    #          ]

    def get_colours(self, response):
        return response.css('.swatch-label::text').extract()

    def get_skus(self, response):
        skus = {}
        for colour in self.get_colours(response):
            for size in self.get_sizes(response):
                skus.update({colour + '_' + size: {'colour': colour,
                                                   'currency': 'EUR',
                                                   'previous_prices': self.get_old_price(response),
                                                   'price': self.get_price(response),
                                                   'size': size
                                                   }
                             })
        return skus

    def get_cautions(self, response):
        return response.css('.content-product-composition span::text').extract()

    def get_sizes(self, response):
        return response.css('.va-size .swatchanchor::text').extract()

    def get_retailer_sku(self, response):
        return response.css('span[itemprop="productID"]::text').extract_first().strip()

    def get_price(self, response):
        try:
            return response.css('.newPrice .currency-price::text').extract_first() + '.' + \
                   response.css('.newPrice .price-decimal::text').extract_first().strip()
        except TypeError:
            return response.css('.actualPrice .pricePlain::text').extract_first() + '.' + \
                   response.css('.actualPrice .price-decimal::text').extract_first().strip()

    def get_old_price(self, response):
        try:
            return response.css('.oldPrice::text').extract_first().strip() + '.' + \
                   response.css('.oldPrice .price-decimal::text').extract_first()
        except TypeError:
            return []

    def get_category(self, response):
        return response.css('.breadcrumb span::text').extract()[1]

    def get_name(self, response):
        return response.css('.name::text').extract_first()

    def get_description(self, response):
        return response.css('.product-desc-long::text').extract()

    def get_image_urls(self, response):
        item = response.meta['item']
        item['image_urls'].extend(response.css('.product-image-link::attr(href)').extract())
        next_url = response.meta['urls'].pop()
        if len(response.meta['urls']) is 1:
            yield Request(next_url, callback=self.get_image_urls, meta={'item': item, 'urls': response.meta['urls']})
        else:
            yield item

    def parse(self, response):
        output = JulesProduct()
        output['name'] = self.get_name(response)
        output['category'] = self.get_category(response)
        output['description'] = self.get_description(response)
        output['care'] = self.get_cautions(response)
        output['name'] = self.get_name(response)
        output['url'] = response.url
        output['skus'] = self.get_skus(response)
        output['gender'] = 'Men'
        output['brand'] = 'Jules'
        output['retailer_sku'] = self.get_retailer_sku(response)
        output['lang'] = 'fra'
        output['retailer'] = 'jules-fr'
        output['date'] = time.strftime("%H:%M:%S")
        output['image_urls'] = []
        img_urls = response.css('.va-color a::attr(href)').extract()
        yield Request(img_urls[0], callback=self.get_image_urls, meta={'item': output, 'urls': img_urls})
