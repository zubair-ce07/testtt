import itertools
import lxml.etree
import re
import ast
from urllib.parse import urlparse
from datetime import datetime
from math import ceil

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import js2xml
import ccy
from parsel import Selector


class JackLemkusScrapper(CrawlSpider):
    name = 'jack_lemkus_scrapper'

    allowed_domains = ['jacklemkus.com']

    start_urls = [
        'https://www.jacklemkus.com/',
        # 'https://www.jacklemkus.com/mens-apparel/t-shirts',
        # 'https://www.jacklemkus.com/accessories/sneaker-cleaner/crep-ultimate-pack',
        # 'https://www.jacklemkus.com/apparel/clrdo-og-sweats-borang',
    ]

    rules = (
        Rule(LinkExtractor(allow=('sneakers', 'mens-apparel', 'womens-apparel', 'kids', 'accessories'),
                           restrict_css='#nav li a:nth-child(2)'), callback='parse_product_category_page'),
    )

    def parse_product_category_page(self, response):
        total_products = response.css('#cust-list > div.amount::text').get().strip().split()[5]
        for page_number in range(1, ceil(int(total_products) / 16) + 1):
            yield response.follow(f'?p={page_number}', self.parse_product_grid)

    def parse_product_grid(self, response):
        product_links = response.css('#products-grid .product-image::attr("href")').getall()
        for product_link in product_links:
            yield response.follow(product_link, self.parse_product)

    def parse_product(self, response):
        trail = JackLemkusScrapper.get_trail(response)

        gender = None
        brand = None
        description = []
        care = []
        care_words = {'synthetic', 'composition'}
        # all text present in description tab and its descendants
        description_tab_data = response.css('#description-tab .std *::text').getall()
        for data in description_tab_data:
            data = data.strip()
            if data != '':
                description.append(data)
                for care_word in care_words:
                    if care_word in data:
                        care.append(data)
                        break
        for tr in response.css('#product-attribute-specs-table tr'):
            entry_id = tr.css('th::text').get().strip()
            entry_value = tr.css('td::text').get().strip()
            description.append(entry_id)
            description.append(entry_value)
            if entry_id == 'Gender':
                gender = re.split(r'[\\ \']', entry_value)[0]
            elif entry_id == 'Item Brand':
                brand = entry_value

        price = JackLemkusScrapper.get_price(response)

        currency = JackLemkusScrapper.get_currency(response)

        market = JackLemkusScrapper.get_market(currency)

        yield {
            'retailer_sku': JackLemkusScrapper.get_retailer_sku(response),
            'trail': trail,
            'gender': gender,
            'category': JackLemkusScrapper.get_category(trail),
            'brand': brand,
            'url': JackLemkusScrapper.get_url(response),
            'date': JackLemkusScrapper.get_date(response),
            'market': market,
            'retailer': JackLemkusScrapper.get_retailer(response, market),
            'url_original': response.url,
            'name': JackLemkusScrapper.get_name(response),
            'description': description,
            'care': care,
            'image_urls': JackLemkusScrapper.get_image_urls(response),
            'skus': JackLemkusScrapper.get_skus(response, price, currency),
            'price': price,
            'currency': currency,
            'spider_name': JackLemkusScrapper.name,
            'crawl_start_time': self.get_crawl_start_time()
        }

    @staticmethod
    def get_retailer_sku(response):
        return response.css('span.sku::text').get().strip()

    @staticmethod
    def get_trail(response):
        trail_anchors = response.css('#breadcrumbs li a')
        return [[trail_anchor.css('::text').get().strip(), trail_anchor.css('::attr("href")').get().strip()]
                for trail_anchor in trail_anchors]

    @staticmethod
    def get_category(trail):
        return [t[0] for t in itertools.islice(trail, 1, None)]

    @staticmethod
    def get_url(response):
        return response.css('head link[rel="canonical"]::attr("href")').get()

    @staticmethod
    def get_date(response):
        date = response.headers["Date"].decode('utf-8')
        return datetime.strptime(date, '%a, %d %b %Y %H:%M:%S GMT').strftime('%Y-%m-%dT%H:%M:%S.%f')

    @staticmethod
    def get_market(currency):
        return ccy.currency(currency).default_country

    @staticmethod
    def get_retailer(response, market):
        return f'{urlparse(response.url).netloc.split(".")[1]}-{market.lower()}'

    @staticmethod
    def get_name(response):
        return response.css('div.product-name h1::text').get().strip()

    @staticmethod
    def get_image_urls(response):
        image_urls = response.css('.product-image-wrapper a::attr("href")').getall()
        return image_urls

    @staticmethod
    def get_skus(response, price, currency):
        product_data = ast.literal_eval(response.css('div.product-data-mine::attr("data-lookup")').get())
        return [{'price': price, 'currency': currency, 'size': data.get('size'), 'out_of_stock': True,
                 'sku_id': data.get('id')} if data['stock_status'] == 0
                else {'price': price, 'currency': currency, 'size': data.get('size'),
                      'sku_id': data.get('id')}
                for data in product_data.values()]

    @staticmethod
    def get_price(response):
        return response.css('.regular-price .price::text').get()

    @staticmethod
    def get_currency(response):
        javascript = response.css('#search_mini_form > div > script::text').get()
        xml = lxml.etree.tostring(js2xml.parse(javascript), encoding='utf-8').decode('utf-8')
        selector = Selector(text=xml)
        return selector.css('property[name="currencycode"] string::text').get()

    def get_crawl_start_time(self):
        return self.crawler.stats._stats['start_time'].strftime('%Y-%m-%dT%H:%M:%S.%f')

# https://stackoverflow.com/questions/44620722/scrapy-crawlspider-crawls-nothing