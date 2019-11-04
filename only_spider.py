from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from w3lib.url import add_or_replace_parameters

from ..items import OnlyItem


class OnlyParser:

    def parse_details(self, response):
        item = OnlyItem()
        currency = self.extract_currency(response)

        item['retailer_sku'] = self.extract_retailor_sku(response)
        item['gender'] = self.extract_gender()
        item['category'] = self.extract_category(response)
        item['brand'] = self.extract_brand()
        item['url'] = self.extract_url(response)
        item['name'] = self.extract_name(response)
        item['description'] = self.extract_description(response)
        item['care'] = self.extract_care(response)
        item['image_urls'] = self.extract_img_urls(response)
        item['skus'] = self.extract_skus(response, currency)

        item['request_queue'] = self.get_color_requests(response)
        if response.css('.length'):
            item['skus'] = []
            item['request_queue'] += self.get_length_requests(response)

        yield self.get_item_or_request_to_yield(item, currency)

    def parse_color(self, response):
        item = response.meta['item']
        currency = response.meta['currency']
        item['image_urls'] += self.extract_img_urls(response)
        if response.css('.length'):
            item['request_queue'] += self.get_length_requests(response)
            item['skus'] += self.extract_skus(response, currency)

        yield self.get_item_or_request_to_yield(item, currency)

    def parse_length(self, response):
        item = response.meta['item']
        currency = response.meta['currency']
        item['skus'] += self.extract_skus(response, currency)

        yield self.get_item_or_request_to_yield(item, currency)

    def get_item_or_request_to_yield(self, item, currency):
        if item['request_queue']:
            request_next = item['request_queue'].pop()
            request_next.meta['item'] = item
            request_next.meta['currency'] = currency
            return request_next

        del item['request_queue']
        return item

    def get_length_requests(self, response):
        size_urls = response.css('.length .swatch__item--selectable a::attr(data-href)').getall()

        return [response.follow(add_or_replace_parameters(url, {'format': 'ajax'}), callback=self.parse_length)
                for url in size_urls]

    def get_color_requests(self, response):
        color_urls = response.css('.swatch__item--selectable-colorpattern a::attr(data-href)').getall()

        return [response.follow(add_or_replace_parameters(url, {'format': 'ajax'}), callback=self.parse_color)
                for url in color_urls]

    def extract_retailor_sku(self, response):
        return response.css('.tfc-fitrec-product::attr(id)').get()

    def extract_gender(self):
        return 'female'

    def extract_category(self, response):
        return eval(response.css('.js-structuredData::text').get())['@graph'][0]['category'].split('>')

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
        common_sku = {'currency': currency}
        common_sku['price'] = response.css('.nonsticky-price__container--visible em::text').get()
        common_sku['previous_price'] = response.css('.nonsticky-price__container--visible del::text').getall()
        common_sku['colour'] = response.css('.swatch__item--selected-colorpattern span::text').get()

        return common_sku

    def extract_skus(self, response, currency):
        common_sku = self.extract_common_sku(response, currency)
        sizes = response.css('.size li')
        length = response.css('.length .swatch__item--selected div::text').get()
        skus = []

        for size_s in sizes:
            sku = common_sku.copy()
            size = size_s.css('div::text').get()
            sku['size'] = f'{length}/{size}' if length else size
            sku['out_of_stock'] = 'true' if 'unavailable' in size_s.css('li::attr(class)').get() else 'false'
            sku['sku_id'] = f'{sku["colour"]}_{sku["size"]}'
            skus.append(sku)

        return skus

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

    only_parser = OnlyParser()
    listing_css = [
        '.menu-top-navigation__link',
        '.paging-controls__next']
    product_css = ['.thumb-link']
    listing_attrs = ['data-href', 'href']

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css, attrs=listing_attrs)),
        Rule(LinkExtractor(restrict_css=product_css), callback=only_parser.parse_details),
    )


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

