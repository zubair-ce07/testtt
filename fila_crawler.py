import itertools
from urllib.parse import urlparse
from datetime import datetime

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import ccy


class FilaCrawler(CrawlSpider):
    name = 'fila'

    allowed_domains = ['fila.com.br']
    start_urls = ['https://www.fila.com.br/']

    rules = (
        Rule(LinkExtractor(deny='outlet', restrict_css=('ol.nav-primary > li > a', 'a.next')), callback='parse'),
        Rule(LinkExtractor(restrict_css='ul.products-grid.products-grid-comum > li div.container-info a'),
             callback='parse_product'),
    )

    def parse(self, response):
        requests = list(super().parse(response))
        trail = response.meta.get('trail', [["", response.url]])
        for request in requests:
            request.meta['trail'] = trail + [[request.meta['link_text'].strip(), request.url]]
            yield request

    def parse_product(self, response):
        retailer_sku = FilaCrawler.get_retailer_sku(response)

        trail = response.meta['trail'][:-1]

        name = FilaCrawler.get_name(response)

        description = FilaCrawler.get_description(response)

        price = FilaCrawler.get_price(response)

        currency = FilaCrawler.get_currency()

        market = FilaCrawler.get_market(currency)

        yield {
            'retailer_sku': retailer_sku,
            'trail': trail,
            'gender': FilaCrawler.get_gender(response.url),
            'category': FilaCrawler.get_category(trail),
            'brand': 'Fila',
            'url': FilaCrawler.get_url(response),
            'date': FilaCrawler.get_date(response),
            'market': market,
            'retailer': FilaCrawler.get_retailer(response, market),
            'url_original': response.url,
            'name': name,
            'description': description,
            'care': FilaCrawler.get_care(description),
            'image_urls': FilaCrawler.get_image_urls(response),
            'skus': FilaCrawler.get_skus(response, retailer_sku, price, currency),
            'price': price,
            'currency': currency,
            'spider_name': FilaCrawler.name,
            'crawl_start_time': self.get_crawl_start_time()
        }

    @staticmethod
    def get_retailer_sku(response):
        return response.css('.wrap-sku > small::text').get().strip()

    @staticmethod
    def get_gender(url):
        genders = {
            'masculina': {'masculina', 'masculino'},
            'feminina': {'feminina', 'feminino'},
            'infantil': {'infantil', 'junior', 'baby'},
            'unisex': {'unisex'}
        }

        name_lowered = url.lower()
        for gender in genders:
            if check_existence(genders[gender], name_lowered):
                return gender
        return ''

    @staticmethod
    def get_description(response):
        description = response.css('div.wrap-long-description > p::text').get()
        return [description] if description is not None else []

    @staticmethod
    def get_care(description):
        care_words = {'sintética', 'composição'}
        return description if len(description) != 0 and check_existence(care_words, description[0].lower()) else []

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
        return list(set(response.css('.product-image-gallery > img::attr("src")').getall()))

    @staticmethod
    def get_skus(response, retailer_sku, price, currency):
        product_sizes = response.css('#configurable_swatch_size .swatch-label::text').getall()
        return [{'price': price, 'currency': currency, 'size': product_size, 'sku_id': f'{retailer_sku}-{product_size}'}
                for product_size in product_sizes]

    @staticmethod
    def get_price(response):
        return response.css('.normal_price_span::text').get()

    @staticmethod
    def get_currency():
        return 'BRL'

    def get_crawl_start_time(self):
        return self.crawler.stats._stats['start_time'].strftime('%Y-%m-%dT%H:%M:%S.%f')


def check_existence(words, text):
    return any(word in text for word in words)
