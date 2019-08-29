import json
import re

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule, Spider
from w3lib.url import add_or_replace_parameter

from calvin.items import CalvinItem


def clean(raw_strs):
    if isinstance(raw_strs, list):
        cleaned_strs = [re.sub('\s+', ' ', st).strip() for st in raw_strs]
        return [st for st in cleaned_strs if st]
    elif isinstance(raw_strs, str):
        return re.sub('\s+', ' ', raw_strs).strip()


class CalvinParseSpider(Spider):
    name = 'calvinparsespider'

    def parse_item(self, response):
        item = CalvinItem()
        item['retailer_sku'] = self.retailer_sku(response)
        item['name'] = self.product_name(response)
        item['gender'] = self.product_gender(response)
        item['category'] = self.product_category(response)
        item['description'] = self.product_description(response)
        item['url'] = self.product_url(response)
        item['brand'] = self.product_brand(response)
        item['care'] = self.product_care(response)
        item['trail'] = self.product_trail(response)
        item['image_urls'] = self.product_image_urls(response)
        item['skus'] = self.product_skus(response)
        return [item] + self.colour_requests(response)

    def colour_requests(self, response):
        color_urls = response.css('.swatch-option ::attr(href)').getall()
        return [Request(color_url, callback=self.parse_item,
                        meta={'trail': response.meta['trail']}) for color_url in color_urls]

    def retailer_sku(self, response):
        return response.css('::attr(data-product-sku)').get()

    def product_name(self, response):
        return response.css('.base::text').get()

    def product_gender(self, response):
        css = 'script:contains("category")'
        return response.css(css).re_first('\'category\': \"(.+?)\"')

    def product_category(self, response):
        return [category[0] for category in response.meta['trail']]

    def product_url(self, response):
        return response.url

    def product_description(self, response):
        return response.css('.data.content ::text').get().split(',')

    def product_brand(self, response):
        return response.css('[itemprop="brand"]::text').get()

    def product_care(self, response):
        css = '[class="attr-label"] + ul ::text'
        return clean(response.css(css).getall())

    def product_trail(self, response):
        return response.meta['trail']

    def product_image_urls(self, response):
        css = 'script:contains("img") ::text'
        img_urls = response.css(css).re('\"img\"\:(.+?),')
        return [url.replace('\\', '') for url in img_urls]

    def product_skus(self, response):
        prev_price_css = '[data-price-type="oldPrice"]::attr(data-price-amount)'
        common_sku = {
            'color': response.css('.current-swatch-text::text').get(),
            'price': response.css('[itemprop="price"]::text').get(),
            'prev_price': response.css(prev_price_css).get()
        }

        skus = {}
        size_css = 'script:contains(\"options\")'
        raw_sizes = response.css(size_css).re_first('\"options\"\:(.+?),\"position')

        for raw_size in json.loads(raw_sizes):
            sku = common_sku.copy()
            sku['size'] = raw_size['label']

            if not int(raw_size['stock_status']):
                sku['out_of_stock'] = True

            sku_id = f'{sku["color"]}_{sku["size"]}'
            skus[sku_id] = sku

        return skus


class CalvinCrawlSpider(CrawlSpider):
    name = 'calvin'
    allowed_domains = ['calvinklein.com.au']
    start_urls = [
        'https://www.calvinklein.com.au/'
    ]
    parse_spider = CalvinParseSpider()
    PAGE_SIZE = 30

    category_css = ['.sub-nav-wrapper ']
    product_css = ['.product-item-photo']

    rules = (
        Rule(LinkExtractor(restrict_css=category_css), callback='parse_categories'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')
    )

    def parse_categories(self, response):
        response.meta['trail'] = self.get_product_trail(response)
        self.parse(response)

        total_pages = int(response.css('.toolbar-number::text').get()) // self.PAGE_SIZE + 2
        for page_number in range(2, total_pages):
            trail = self.get_product_trail(response)
            pagination_url = add_or_replace_parameter(response.url, 'p', page_number)
            yield Request(pagination_url, callback=self.parse, meta={'trail': trail})

    def parse_item(self, response):
        return self.parse_spider.parse_item(response)

    def get_product_trail(self, response):
        categories_css = '[data-container="body"]::attr(class)'
        categories = response.css(categories_css).re_first('categorypath-(.+?) ', '')
        return categories.replace('-', ' '), response.url
