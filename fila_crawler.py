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

    listings_css = ('ol.nav-primary > li > a', 'a.next')

    currency = 'BRL'
    brand = 'Fila'
    retailer = 'fila-br'

    rules = (
        Rule(LinkExtractor(deny='outlet', restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css='ul.products-grid.products-grid-comum > li div.container-info a'),
             callback='parse_product'),
    )

    def parse(self, response):
        trail = response.meta.get('trail', [["", response.url]])
        for request in super().parse(response):
            request.meta['trail'] = trail + [[request.meta['link_text'].strip(), request.url]]
            yield request

    def parse_product(self, response):
        product = dict()

        product['retailer_sku'] = self.extract_retailer_sku(response)
        product['trail'] = response.meta['trail'][:-1]
        product['gender'] = self.extract_gender(response.url)
        product['category'] = self.extract_category(product['trail'])
        product['brand'] = FilaCrawler.brand
        product['url'] = self.extract_url(response)
        product['date'] = self.extract_date(response)
        product['currency'] = FilaCrawler.currency
        product['market'] = self.extract_market(product['currency'])
        product['retailer'] = FilaCrawler.retailer
        product['url_original'] = response.url
        product['name'] = self.extract_name(response)
        product['description'] = self.extract_description(response)
        product['care'] = self.extract_care(product['description'])
        product['image_urls'] = self.extract_image_urls(response)
        product['price'] = self.extract_price(response)
        product['skus'] = self.extract_skus(response, product['retailer_sku'], product['price'], product['currency'])
        product['spider_name'] = FilaCrawler.name
        product['crawl_start_time'] = self.extract_crawl_start_time()

        yield product

    def extract_retailer_sku(self, response):
        return response.css('.wrap-sku > small::text').get().strip()

    def extract_gender(self, url):
        genders = {
            'masculina': {'masculina', 'masculino'},
            'feminina': {'feminina', 'feminino'},
            'infantil': {'infantil', 'junior', 'baby'},
            'unisex': {'unisex'}
        }

        url_lowercase = url.lower()
        for gender in genders:
            if check_existence(genders[gender], url_lowercase):
                return gender
        return ''

    def extract_description(self, response):
        description = response.css('div.wrap-long-description > p::text').get()
        return [description] if description is not None else []

    def extract_care(self, description):
        care_words = {'sintética', 'composição'}
        return description if len(description) != 0 and check_existence(care_words, description[0].lower()) else []

    def extract_category(self, trail):
        return [t[0] for t in itertools.islice(trail, 1, None)]

    def extract_url(self, response):
        return response.css('head link[rel="canonical"]::attr("href")').get()

    def extract_date(self, response):
        date = response.headers["Date"].decode('utf-8')
        return datetime.strptime(date, '%a, %d %b %Y %H:%M:%S GMT').strftime('%Y-%m-%dT%H:%M:%S.%f')

    def extract_market(self, currency):
        return ccy.currency(currency).default_country

    def extract_retailer(self, response, market):
        return f'{urlparse(response.url).netloc.split(".")[1]}-{market.lower()}'

    def extract_name(self, response):
        return response.css('div.product-name h1::text').get().strip()

    def extract_image_urls(self, response):
        return list(set(response.css('.product-image-gallery > img::attr("src")').getall()))

    def extract_skus(self, response, retailer_sku, price, currency):
        price_currency_dict = {'price': price, 'currency': currency}

        product_sizes = response.css('#configurable_swatch_size .swatch-label::text').getall()
        return [{**price_currency_dict,
                 'size': product_size,
                 'sku_id': f'{retailer_sku}-{product_size}'}
                for product_size in product_sizes]

    def extract_price(self, response):
        return response.css('.normal_price_span::text').get()

    def extract_crawl_start_time(self):
        return self.crawler.stats._stats['start_time'].strftime('%Y-%m-%dT%H:%M:%S.%f')


def check_existence(words, text):
    return any(word in text for word in words)
