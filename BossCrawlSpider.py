import re

from scrapy import Item, Field
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Spider
from scrapy.spiders import Rule


def clean(raw_strs):
    if isinstance(raw_strs, list):
        cleaned_strs = [re.sub('\s+', ' ', st).strip() for st in raw_strs]
        return [st for st in cleaned_strs if st]
    elif isinstance(raw_strs, str):
        return re.sub('\s+', ' ', raw_strs).strip()


class BossItem(Item):
    retailer_sku = Field()
    gender = Field()
    name = Field()
    category = Field()
    url = Field()
    brand = Field()
    description = Field()
    care = Field()
    image_urls = Field()
    stock = Field()
    color = Field()
    price = Field()
    skus = Field()
    requests = Field()


class BossParseSpider(Spider):
    name = 'bossparse'

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
        item['skus'] = self.product_skus(response)

        item['requests'] = self.colour_requests(response)
        return self.next_request_or_item(item)

    def colour_requests(self, response):
        color_urls = response.css('.swatch-list__image--is-large ::attr(href)').getall()
        return [response.follow(url, callback=self.parse_color)
                for url in color_urls if url not in response.url]

    def parse_color(self, response):
        item = response.meta['item']
        item['image_urls'].extend(self.images_url(response))
        item['skus'].update(self.product_skus(response))
        return self.next_request_or_item(item)

    def product_skus(self, response):
        sizes_sel = response.css('.product-stage__choose-size--container a')
        color = clean(response.css('.product-stage__control-item__label'
                                   '--variations ::text').getall()[2])
        common_sku = {
            'color': color,
            'price': clean(response.css('.product-price--price-sales ::text').get()),
            'previous_price': clean(response.css('.product-price--price-'
                                                 'standard s ::text').getall())
        }
        skus = {}
        if not sizes_sel:
            size = 'One_Size'
            key = f'{color}_{size}'
            skus[key] = {
                'out_of_stock': False,
                'size': size
            }
            skus[key].update(common_sku)

            return skus

        for size_sel in sizes_sel:
            size = clean(size_sel.css('span ::text').getall())[0]
            key = f'{color}_{size}'
            skus[key] = {
                'out_of_stock': not bool(size_sel.css('::attr(href)').get()),
                'size': size
            }
            skus[key].update(common_sku)

        return skus

    def next_request_or_item(self, item):
        if item['requests']:
            request = item['requests'].pop()
            request.meta['item'] = item
            return request

        item.pop('requests', None)
        return item

    def retailer_sku(self, response):
        return response.css('script:contains("productSku")').re_first("productSku\":\"(.+?)\"")

    def product_gender(self, response):
        return response.css('script:contains("productGender")').re_first("productGender\":\"(.+?)\"")

    def product_name(self, response):
        return response.css('.font__h2 ::text').get()

    def product_category(self, response):
        return response.css('.breadcrumb__title ::text').getall()[1:4]

    def product_url(self, response):
        return response.url

    def product_brand(self, response):
        return response.css('[itemprop= "brand"] ::attr(content)').get() or "BOSS"

    def product_description(self, response):
        return clean(response.css('.description div ::text').get())

    def product_care(self, response):
        return response.css('.accordion__item__icon ::text').getall()

    def images_url(self, response):
        return response.css('.slider-item--thumbnail-image ::attr(src)').getall()


class BossCrawlSpider(CrawlSpider):
    parse_spider = BossParseSpider()
    name = 'bosscrawl'
    allowed_domains = ['hugoboss.com']
    start_urls = [
        'https://www.hugoboss.com/uk/home'
    ]

    listing_and_pagination_css = ['.main-header', '.pagingbar__next']
    product_css = ['.product-tile__link']

    rules = (
        Rule(LinkExtractor(restrict_css=listing_and_pagination_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css), callback=parse_spider.parse_item),
    )

