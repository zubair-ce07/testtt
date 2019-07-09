import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule


class BossItem(scrapy.Item):
    retailer_sku = scrapy.Field()
    gender = scrapy.Field()
    name = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()
    brand = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    image_urls = scrapy.Field()
    stock = scrapy.Field()
    color = scrapy.Field()
    price = scrapy.Field()
    skus = scrapy.Field()


class BossSpider(CrawlSpider):
    name = 'hugoboss'
    allowed_domains = ['hugoboss.com']
    start_urls = [
        'https://www.hugoboss.com/uk/home',
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=('.main-header'))),
        Rule(LinkExtractor(allow=('\/uk\/(.+?)\?cgid=\d+'), restrict_css=('.search-result-items')),
             callback='parse_item'),
    )

    def parse_item(self, response):
        item = BossItem()
        item['retailer_sku'] = self.retailer_sku(response)
        item['gender'] = self.product_gender(response)
        item['name'] = self.product_name(response)
        item['category'] = self.product_category(response)
        item['url'] = self.product_url(response)
        item['brand'] = self.product_brand(response)
        item['description'] = self.product_description(response)
        item['care'] = self.product_care(response)
        item['image_urls'] = self.images_url(response)

        for colors in response.css('.swatch-list__image--is-large ::attr(data-colorcode)').getall():
            size_url = re.sub(r'_\d+\.html', '_' + colors.split('_')[0] + '.html', response.url)

            yield response.follow(url=size_url + "&Quantity=1&origin=&format=ajax",
                                  callback=self.parse_size_price, meta={'color': colors.split('_')[1], 'item': item})

    def retailer_sku(self, response):
        return response.css('script[type="text/javascript"]').re("productSku\":\"(.+?)\"")[0]

    def product_gender(self, response):
        return response.css('script[type="text/javascript"]').re("productGender\":\"(.+?)\"")[0]

    def product_name(self, response):
        return response.css('.font__h2 ::text').get()

    def product_category(self, response):
        return response.css('.breadcrumb__title ::text').getall()[1:4]

    def product_url(self, response):
        return response.url

    def product_brand(self, response):
        return response.css('meta[itemprop= "brand"] ::attr(content)').get()

    def product_description(self, response):
        return self.clean(response.css('.description div ::text').get())

    def product_care(self, response):
        return response.css('.accordion__item__icon ::text').getall()

    def images_url(self, response):
        return response.css('.slider-item--thumbnail-image ::attr(src)').getall()

    def clean(self, raw_data):
        description = []

        if isinstance(raw_data, list):
            for string in raw_data:
                if re.sub('\s+', '', string):
                    description.append(re.sub('\s+', '', string))

            return description

        if re.sub('\s+', '', raw_data):
            return re.sub('\s+', '', raw_data)

    def parse_size_price(self, response):

        item = response.meta['item']
        color = response.meta['color']
        price = self.clean(response.css('.product-price--price-sales ::text').get())
        previous_price = self.clean(response.css('.product-price--price-standard s ::text').getall())
        raw_skus = {}
        for size in response.css('.product-stage__choose-size--container '
                                 '[disabled!="disabled"] ::attr(title)').getall():
            raw_skus.update({f'{color}_{size}': {
                'color': color,
                'price': price,
                'previous_price': previous_price,
                'size': size
            }})
        item['skus'] = raw_skus
        yield item

