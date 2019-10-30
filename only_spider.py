import re

from scrapy.spiders import CrawlSpider
from scrapy import Request
from w3lib.url import add_or_replace_parameters

from ..items import OnlyItem


class OnlyParser:

    def parse_details(self, response):
        item = OnlyItem()

        item['retailer_sku'] = self.extract_retailor_sku(response)
        item['gender'] = self.extract_gender()
        item['category'] = self.extract_category(response)
        item['brand'] = self.extract_brand()
        item['url'] = self.extract_url(response)
        item['name'] = self.extract_name(response)
        item['description'] = self.extract_description(response)
        item['care'] = self.extract_care(response)
        item['image_urls'] = self.extract_img_urls(response)
        item['currency'] = self.extract_currency(response)
        item['skus'] = []

        item['request_queue'] = self.get_color_requests(response)
        item['request_queue'] += self.get_size_requests(response)

        yield self.get_item_or_request_to_yield(item)

    def parse_color(self, response):
        item = response.meta['item']
        item['request_queue'] += self.get_size_requests(response)
        item['image_urls'] += self.extract_img_urls(response)

        yield self.get_item_or_request_to_yield(item)

    def parse_size(self, response):
        item = response.meta['item']
        item['skus'] += self.extract_skus(response, item['currency'])

        yield self.get_item_or_request_to_yield(item)

    def get_item_or_request_to_yield(self, item):
        if item['request_queue']:
            request_next = item['request_queue'].pop()
            request_next.meta['item'] = item
            return request_next

        del item['currency']
        del item['request_queue']
        return item

    def get_size_requests(self, response):
        size_urls = response.css('.size .swatch__item--selectable a::attr(data-href)').getall()

        return [Request(add_or_replace_parameters(url, {'format': 'ajax'}), callback=self.parse_size)
                for url in size_urls]

    def get_color_requests(self, response):
        color_urls = response.css('.swatch__item--selectable-colorpattern a::attr(data-href)').getall()

        return [Request(add_or_replace_parameters(url, {'format': 'ajax'}), callback=self.parse_color)
                for url in color_urls]

    def extract_retailor_sku(self, response):
        return response.css('.tfc-fitrec-product::attr(id)').get()

    def extract_gender(self):
        return 'female'

    def extract_category(self, response):
        return re.search('(?<=on/)(.+)', response.url).group().split('/')[:-1]

    def extract_brand(self):
        return 'only'

    def extract_url(self, response):
        return response.url

    def extract_name(self, response):
        return response.css('.product-name--visible::text').get()

    def extract_description(self, response):
        return self.clean(response.css('.pdp-description__text__short::text').getall())

    def extract_care(self, response):
        return self.clean(response.css('.pdp-description__list ::text').getall())

    def extract_img_urls(self, response):
        return response.css('.product-images__main__image img::attr(data-secondary-src)').getall()

    def extract_currency(self, response):
        return response.css('[property="og:price:currency"]::attr(content)').get()

    def extract_common_sku(self, response, currency):
        size = response.css('.size .swatch__item--selected')
        common_sku = {'currency': currency}
        common_sku['price'] = response.css('.nonsticky-price__container--visible em::text').get()
        common_sku['previous_price'] = response.css('.nonsticky-price__container--visible del::text').getall()
        common_sku['colour'] = response.css('.swatch__item--selected-colorpattern span::text').get()
        common_sku['size'] = size.css('div::text').get()
        common_sku['out_of_stock'] = 'true' if 'unavailable' in size.css('li::attr(class)').get() else 'false'
        common_sku['sku_id'] = f'{common_sku["colour"]}_{common_sku["size"]}'

        return common_sku

    def extract_skus(self, response, currency):
        common_sku = self.extract_common_sku(response, currency)
        length_sizes = response.css('.swatch.length li')
        skus = []
        for length in length_sizes:
            sku = common_sku.copy()
            sku['size'] = f'{length.css("div::text").get()}/{sku["size"]}'
            sku['out_of_stock'] = 'true' if 'unavailable' in length.css('li::attr(class)').get() else 'false'
            sku['sku_id'] = f'{sku["colour"]}_{sku["size"]}'
            skus.append(sku)

        return skus if skus else [common_sku]

    def clean(self, list_to_strip):
        if isinstance(list_to_strip, str):
            return list_to_strip.strip()
        return [str_to_strip.strip() for str_to_strip in list_to_strip if str_to_strip.strip()]


class OnlySpider(CrawlSpider):
    name = 'onlySpider'
    allowed_domains = ['only.com']
    start_urls = [
        'https://www.only.com/gb/en/home',
    ]
    detail_parser = OnlyParser()

    def parse(self, response):
        categories = response.css('.menu-top-navigation__link::attr(href)').getall()
        for category in categories:
            yield response.follow(category, callback=self.parse_category)

    def parse_category(self, response):
        products = response.css('.thumb-link::attr(href)').getall()
        next_page = response.css('.paging-controls__next::attr(data-href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_category)
        for product in products:
            yield response.follow(product, callback=self.detail_parser.parse_details)


class OnlyItem(scrapy.Item):
    retailer_sku = scrapy.Field()
    gender = scrapy.Field()
    category = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()
    request_queue = scrapy.Field()
    currency = scrapy.Field()

