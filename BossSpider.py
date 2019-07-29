import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule


def clean(raw_data):
    if isinstance(raw_data, list):
        return [re.sub('\s+', ' ', data).strip() for data in raw_data
                if re.sub('\s+', ' ', data).strip()]
    elif isinstance(raw_data, str):
        return re.sub('\s+', ' ', raw_data).strip()
    return ''


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
    requests = scrapy.Field()


class BossSpider(CrawlSpider):
    name = 'boss'
    allowed_domains = ['hugoboss.com']
    start_urls = [
        'https://www.hugoboss.com/uk/home'
    ]

    listing_css = '.main-header'
    product_css = '.product-tile__link'
    next_page_css = '.pagingbar__next'

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=next_page_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item'),
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
        item['skus'] = {}
        item['requests'] = self.colors_queues(response)

        return self.next_request_or_item(item)

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
        return response.css('meta[itemprop= "brand"] ::attr(content)').get() or "BOSS"

    def product_description(self, response):
        return clean(response.css('.description div ::text').get())

    def product_care(self, response):
        return response.css('.accordion__item__icon ::text').getall()

    def images_url(self, response):
        return response.css('.slider-item--thumbnail-image ::attr(src)').getall()

    def colors_queues(self, response):
        color_queue = response.css('.swatch-list__image--is-large ::attr(href)').getall()
        return [response.follow(color_url, callback=self.parse_size)
                for color_url in color_queue]

    def parse_size(self, response):

        item = response.meta['item']
        sizes = response.css('.product-stage__choose-size--container a')

        for a in sizes:
            if a.css('::attr(href)'):
                item['requests'].append(response.follow(a.css('::attr(href)').get(), callback=self.parse_sku))
            else:
                item['requests'].append(
                    response.follow(response.url, callback=self.parse_sku, dont_filter=True,
                                    meta={'size': clean(a.css('.swatch-list__size ::text').get())}))

        return self.next_request_or_item(item)

    def parse_sku(self, response):
        size = None
        out_of_stock = False
        if 'size' in response.meta:
            size = response.meta['size']
            out_of_stock = True

        item = response.meta['item']
        color = clean(response.css('.product-stage__control-item__label--variations '
                                   '::text').getall()[2])
        price = clean(response.css('.product-price--price-sales ::text').get())
        previous_price = clean(response.css('.product-price--price-standard s ::text').getall())
        if not size:
            size = self.product_size(response)

        item['skus'].update({f'{color}_{size}': {
            'color': color,
            'price': price,
            'out_of_stock': out_of_stock,
            'previous_price': previous_price,
            'size': size
        }})

        return self.next_request_or_item(item)

    def product_size(self, response):
        size = clean(response.css('.product-stage__control-item__selcted-size ::text').get())
        if size:
            return size
        return 'One Size'

    def next_request_or_item(self, item):
        if item['requests']:
            request = item['requests'].pop()
            request.meta.update({'item': item})
            return request
        item.pop('requests', None)
        return item

