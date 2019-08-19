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

    listings_css = ['.main-header', '.pagingbar__next']
    product_css = ['.product-tile__link']
    one_size_sel = [Selector(text='<span><span href="#">One_Size</span></span>')]

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item'),
    )

    def parse_item(self, response):
        raw_product = self.get_raw_product(response)
        item = BossItem()
        item['retailer_sku'] = self.retailer_sku(raw_product)
        item['gender'] = self.product_gender(raw_product)
        item['name'] = self.product_name(raw_product)
        item['category'] = self.product_category(raw_product)
        item['url'] = self.product_url(response)
        item['brand'] = self.product_brand(raw_product)
        item['description'] = self.product_description(response)
        item['care'] = self.product_care(response)
        item['image_urls'] = self.images_url(response)
        item['skus'] = self.product_skus(response)

        item['requests'] = self.colour_requests(response)
        return self.next_request_or_item(item)

    def get_raw_product(self, response):
        raw_sku_css = 'script:contains("productSku")::text'
        return json.loads(response.css(raw_sku_css).re_first('push\((.+?)\)'))

    def colour_requests(self, response):
        colour_css = '.swatch-list__image--is-large ::attr(href)'
        color_urls = response.css(colour_css).getall()
        return [response.follow(url, callback=self.parse_color)
                for url in color_urls if url not in response.url]

    def parse_color(self, response):
        item = response.meta['item']
        item['image_urls'] += self.images_url(response)
        item['skus'].update(self.product_skus(response))
        return self.next_request_or_item(item)

    def product_skus(self, response):
        colour_css = '.product-stage__control-item__label--variations ::text'
        sizes_sel = response.css('.product-stage__choose-size--container a')
        color = clean(response.css(colour_css).getall()[2])

        common_sku = {
            'color': color,
            'price': clean(response.css('.product-price--price-sales ::text').get()),
            'previous_price': clean(response.css('.product-price--price-standard s ::text').getall())}
        skus = {}

        for size_sel in sizes_sel or self.one_size_sel:
            sku = common_sku.copy()
            sku['size'] = clean(size_sel.css('span span::text').get())

            if not bool(size_sel.css('::attr(href)').get()):
                sku['out_of_stock'] = True
            skus[f'{sku["color"]}_{sku["size"]}'] = sku

        return skus

    def next_request_or_item(self, item):
        if item['requests']:
            request = item['requests'].pop()
            request.meta['item'] = item
            return request

        item.pop('requests', None)
        return item

    def retailer_sku(self, raw_product):
        return raw_product['productSku']

    def product_gender(self, raw_product):
        return raw_product['productGender']

    def product_name(self, raw_product):
        return raw_product['productName']

    def product_category(self, raw_product):
        return raw_product['productCategory'].split(' ')

    def product_url(self, response):
        return response.url

    def product_brand(self, raw_product):
        return raw_product['productBrand']

    def product_description(self, response):
        return clean(response.css('.description div ::text').get().split('.'))

    def product_care(self, response):
        return response.css('.materialCare .accordion__item__icon ::text').getall()

    def images_url(self, response):
        return response.css('.slider-item--thumbnail-image ::attr(src)').getall()

