import itertools
import re
import ast
from urllib.parse import urlparse
from datetime import datetime

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import ccy


class JackLemkusCrawler(CrawlSpider):
    name = 'jacklemkus'

    allowed_domains = ['jacklemkus.com']
    start_urls = ['https://www.jacklemkus.com/']

    rules = (
        Rule(LinkExtractor(deny='how-to-order', restrict_css=('#nav > li > a', 'a.next')), callback='parse'),
        Rule(LinkExtractor(restrict_css='.products-grid > li > .product-image'), callback='parse_product'),
    )

    def parse(self, response):
        requests = list(super().parse(response))
        trail = response.meta.get('trail', [["", response.url]])
        for request in requests:
            request.meta['trail'] = trail + [[request.meta['link_text'].strip(), request.url]]
            yield request

    def parse_product(self, response):
        trail = response.meta['trail'][:-1]

        gender, brand, description, care = JackLemkusCrawler.get_gender_brand_description_care(response)

        price = JackLemkusCrawler.get_price(response)

        currency = JackLemkusCrawler.get_currency(response)

        market = JackLemkusCrawler.get_market(currency)

        yield {
            'retailer_sku': JackLemkusCrawler.get_retailer_sku(response),
            'trail': trail,
            'gender': gender,
            'category': JackLemkusCrawler.get_category(trail),
            'brand': brand,
            'url': JackLemkusCrawler.get_url(response),
            'date': JackLemkusCrawler.get_date(response),
            'market': market,
            'retailer': JackLemkusCrawler.get_retailer(response, market),
            'url_original': response.url,
            'name': JackLemkusCrawler.get_name(response),
            'description': description,
            'care': care,
            'image_urls': JackLemkusCrawler.get_image_urls(response),
            'skus': JackLemkusCrawler.get_skus(response, price, currency),
            'price': price,
            'currency': currency,
            'spider_name': JackLemkusCrawler.name,
            'crawl_start_time': self.get_crawl_start_time()
        }

    @staticmethod
    def get_retailer_sku(response):
        return response.css('span.sku::text').get().strip()

    @staticmethod
    def get_gender_brand_description_care(response):
        gender = None
        brand = None
        description = []
        care = []
        care_words = {'synthetic', 'composition'}

        # processing description tab data
        for data in JackLemkusCrawler.get_description_tab_data(response):
            description.append(data)
            for care_word in care_words:
                if care_word in data:
                    care.append(data)
                    break

        # processing more info tab data
        for tr in response.css('#product-attribute-specs-table tr'):
            entry_id = tr.css('th::text').get().strip()
            entry_value = tr.css('td::text').get().strip()
            description.append(entry_id)
            description.append(entry_value)
            if entry_id == 'Gender':
                gender = re.split(r'[\\ \']', entry_value)[0]
            elif entry_id == 'Item Brand':
                brand = entry_value

        return gender, brand, description, care

    @staticmethod
    def get_description_tab_data(response):
        # all text present in description tab and its descendants
        description_tab_data = response.css('#description-tab .std *::text').getall()
        for data in description_tab_data:
            data = data.strip()
            if data != '':
                yield data

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
        return [{'price': price, 'currency': currency, 'size': data.get('size'),
                 'out_of_stock': not data['stock_status'], 'sku_id': data.get('id')}
                for data in product_data.values()]

    @staticmethod
    def get_price(response):
        return response.css('.regular-price .price::text').get()

    @staticmethod
    def get_currency(response):
        auto_complete_options_script = response.css('#search_mini_form > div > script::text').get()
        return re.search("currencycode:'(.+?)'", auto_complete_options_script).group(1)

    def get_crawl_start_time(self):
        return self.crawler.stats._stats['start_time'].strftime('%Y-%m-%dT%H:%M:%S.%f')
