import json
import re
from urllib.parse import parse_qs, urlparse

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule, Spider
from w3lib.url import add_or_replace_parameter

from kleineskarussell.items import KleineskarussellItem


def clean(raw_strs):
    if isinstance(raw_strs, list):
        cleaned_strs = [re.sub('\s+', ' ', st).strip() for st in raw_strs]
        return [st for st in cleaned_strs if st]
    elif isinstance(raw_strs, str):
        return re.sub('\s+', ' ', raw_strs).strip()


class KleineParseSpider(Spider):
    name = 'Kleineparse'

    def parse_item(self, response):
        item = KleineskarussellItem()
        item['retailer_sku'] = self.retailer_sku(response)
        item['name'] = self.product_name(response)
        item['category'] = self.product_category(response)
        item['gender'] = self.product_gender(item['category'])
        item['description'] = self.product_description(response)
        item['url'] = self.product_url(response)
        item['brand'] = self.product_brand(response)
        item['care'] = self.product_care(response)
        item['image_urls'] = self.product_image_urls(response)
        item['skus'] = self.product_skus(response)

        return item

    def retailer_sku(self, response):
        return response.css('script:contains("sku")::text').re_first('sku\: \[\'(.+?)\'')

    def product_name(self, response):
        return response.css('.product-name h1::text').get()

    def product_gender(self, category):
        if 'Mama' in category:
            return 'Women'
        return 'Unisex-Kids'

    def product_category(self, response):
        css = 'script:contains("config")::text'
        return clean(response.css(css).re_first('category":\s"(.+?)"').split('|'))

    def product_url(self, response):
        return response.url

    def product_description(self, response):
        return clean(response.css('.short-description ::text').getall())

    def product_brand(self, response):
        return response.css('.product-manufacturer .h2::text').get()

    def product_care(self, response):
        care_list = ['%', '°']
        raw_cares = response.css('.tab-content .std ::text').getall()
        return [raw_care for symbol in care_list for raw_care in clean(raw_cares)
                if symbol in raw_care]

    def product_image_urls(self, response):
        return [url.split(',')[0].split(' ')[0]
                for url in response.css('.gallery-image::attr(srcset)').getall()]

    def product_skus(self, response):
        common_sku = {
            'price': response.css('script:contains("config")::text').re_first('price":\s"(.+?)"'),
        }

        color = response.css('h5:contains("Farbe") + p::text').get()
        previous_prices = response.css('h5:contains("Farbe") + p::text').get()

        if color:
            common_sku['color'] = color

        if previous_prices:
            common_sku['previous_prices'] = [clean(previous_prices)]

        skus = {}
        for raw_size in self.get_raw_sizes(response):
            common_sku['size'] = raw_size['label']
            sku_id = f'{common_sku.get("color", "OneColor")}_{common_sku["size"]}'
            skus[sku_id] = common_sku

        return skus

    def get_raw_sizes(self, response):
        size_css = 'script:contains("spConfig")'
        one_size = '{"attributes":{"155":{"options":[{"label": "OneSize"}]}}}'
        raw_json = json.loads(response.css(size_css).re_first('fig\((.+?)\)', one_size))
        return raw_json['attributes']['155']['options']


class KleineCrawlSpider(CrawlSpider):
    name = 'kleine'
    allowed_domains = ['kleineskarussell.de']
    start_urls = [
        'https://www.kleineskarussell.de/'
    ]
    parse_spider = KleineParseSpider()

    listings_css = ['.nav-primary']
    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse_category'),
    )

    def parse_category(self, response):
        parsed_url = urlparse(response.url).query
        url_page = int(parse_qs(parsed_url).get('p', [1])[0])
        current_page = int(response.css('.current::text').get(1))

        if url_page is not current_page:
            return

        yield from self.parse_products(response)
        pagination_url = add_or_replace_parameter(response.url, 'p', current_page + 1)
        yield Request(pagination_url, callback=self.parse_category)

    def parse_products(self, response):
        return [Request(product_url, callback=self.parse_spider.parse_item)
                for product_url in response.css('.product-image::attr(href)').getall()]

