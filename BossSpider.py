import json
import re

from scrapy.selector import Selector
from scrapy import Item, Field
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


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
    skus = Field()
    requests = Field()


class BossSpider(CrawlSpider):
    name = 'boss'
    allowed_domains = ['hugoboss.com']
    start_urls = [
        'https://www.hugoboss.com/uk/home'
    ]

    listing_and_pagination_css = ['.main-header', '.pagingbar__next']
    product_css = ['.product-tile__link']
    one_size_sel = [Selector(text='<span><span href="#">One_Size</span></span>')]

    rules = (
        Rule(LinkExtractor(restrict_css=listing_and_pagination_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item'),
    )

    def parse_item(self, response):
        product_json = json.loads(response.css('script:contains("productSku")'
                                               '::text').re_first('push\((.+?)\)'))
        item = BossItem()
        item['retailer_sku'] = self.retailer_sku(product_json)
        item['gender'] = self.product_gender(product_json)
        item['name'] = self.product_name(product_json)
        item['category'] = self.product_category(product_json)
        item['url'] = self.product_url(response)
        item['brand'] = self.product_brand(product_json)
        item['description'] = self.product_description(response)
        item['care'] = self.product_care(response)
        item['image_urls'] = self.images_url(response)
        item['skus'] = self.product_skus(response)

        item['requests'] = self.colour_requests(response)
        return self.next_request_or_item(item)

    def colour_requests(self, response):
        color_urls = response.css('.swatch-list__image--is-large '
                                  '::attr(href)').getall()
        return [response.follow(url, callback=self.parse_color)
                for url in color_urls if url not in response.url]

    def parse_color(self, response):
        item = response.meta['item']
        item['image_urls'] += self.images_url(response)
        item['skus'].update(self.product_skus(response))
        return self.next_request_or_item(item)

    def product_skus(self, response):
        sizes_sel = response.css('.product-stage__choose-size--container a')
        color = clean(response.css('.product-stage__control-item__label--variations '
                                   '::text').getall()[2])

        common_sku = {
            'color': color,
            'price': clean(response.css('.product-price--price-sales ::text').get()),
            'previous_price': clean(response.css('.product-price--price-'
                                                 'standard s ::text').getall())}
        skus = {}

        for size_sel in sizes_sel or self.one_size_sel:
            sku = common_sku.copy()
            sku['size'] = clean(size_sel.css('span span::text').get())
            sku['out_of_stock'] = not bool(size_sel.css('::attr(href)').get())
            skus[f'{sku["color"]}_{sku["size"]}'] = sku

        return skus

    def next_request_or_item(self, item):
        if item['requests']:
            request = item['requests'].pop()
            request.meta['item'] = item
            return request

        item.pop('requests', None)
        return item

    def retailer_sku(self, product_json):
        return product_json['productSku']

    def product_gender(self, product_json):
        return product_json['productGender']

    def product_name(self, product_json):
        return product_json['productName']

    def product_category(self, product_json):
        return product_json['productCategory'].split(' ')

    def product_url(self, response):
        return response.url

    def product_brand(self, product_json):
        return product_json['productBrand']

    def product_description(self, response):
        return clean(response.css('.description div ::text').get().split('.'))

    def product_care(self, response):
        return response.css('.materialCare .accordion__item__icon ::text').getall()

    def images_url(self, response):
        return response.css('.slider-item--thumbnail-image ::attr(src)').getall()

