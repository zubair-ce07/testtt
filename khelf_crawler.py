from math import ceil
import itertools
from datetime import datetime

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import ccy


class KhelfCrawler(CrawlSpider):
    name = 'khelf'

    allowed_domains = ['khelf.com.br']
    start_urls = ['https://www.khelf.com.br/']

    listings_css = ['#nav > li > a']
    products_css = ['#listProduct > li > div > div.figure > a']

    currency = 'BRL'
    retailer = 'khelf-br'

    link_category_map = {
        'https://www.khelf.com.br/feminino-1.aspx/c': 1,
        'https://www.khelf.com.br/masculino-3.aspx/c': 3,
        'https://www.khelf.com.br/acessorios-4.aspx/c': 4
    }

    rules = (
        Rule(LinkExtractor(allow=('feminino', 'masculino', 'acessorios'), restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_product'),
    )

    def parse(self, response):
        trail = response.meta.get('trail', [["", response.url]])
        for request in super().parse(response):
            request.meta['trail'] = trail + [[request.meta['link_text'].strip(), request.url]]
            yield request

        # pagination
        category = self.link_category_map.get(response.url)
        if category is not None:
            category_products_count = int(response.css('.filter-details strong:last-child::text').get())
            for page_number in range(1, ceil(int(category_products_count) / 21) + 1):
                link = (f'https://www.khelf.com.br/categoria/1/{category}/0//MaisRecente/Decrescente/21/{page_number}'
                        f'//0/0/.aspx')
                link_trail = trail + [['>', link]]
                yield response.follow(link, meta={'trail': link_trail})

    def parse_product(self, response):
        product = {}

        product['retailer_sku'] = self.extract_retailer_sku(response)
        product['trail'] = response.meta['trail'][:-1]
        product['description'] = self.extract_description(response)
        product['gender'] = self.extract_gender(response.url)
        product['category'] = self.extract_category(product['trail'])
        # product['brand'] = self.extract_brand(response)
        product['url'] = self.extract_url(response)
        product['date'] = self.extract_date(response)
        product['price'] = self.extract_price(response)
        product['currency'] = self.currency
        product['market'] = self.extract_market()
        product['retailer'] = self.retailer
        product['url_original'] = response.url
        product['name'] = self.extract_name(response)
        product['care'] = self.extract_care(response)
        # product['image_urls'] = self.extract_image_urls(response)
        # product['skus'] = self.extract_skus(response, product['price'])
        product['spider_name'] = self.name
        product['crawl_start_time'] = self.extract_crawl_start_time()

        yield product

    def extract_retailer_sku(self, response):
        return response.css('#liCodigoInterno > span::text').get().strip()

    def extract_gender(self, url):
        genders = {
            'masculina': {'masculina', 'masculino'},
            'feminina': {'feminina', 'feminino'},
            'infantil': {'infantil', 'junior', 'baby'},
        }

        url_lowercase = url.lower()
        for gender in genders:
            if check_words_existence(genders[gender], url_lowercase):
                return gender
        return 'unisex'

    # def extract_brand(self, response):
    #     brands_x = ('//*[@id="product-attribute-specs-table"]/tbody/tr/th[contains(text(),"Item Brand")]/'
    #                 'following-sibling::td/text()')
    #     return response.xpath().get()

    def extract_category(self, trail):
        return [t[0] for t in itertools.islice(trail, 1, None)]

    def extract_url(self, response):
        return response.css('head link[rel="canonical"]::attr("href")').get()

    def extract_date(self, response):
        date = response.headers["Date"].decode('utf-8')
        return datetime.strptime(date, '%a, %d %b %Y %H:%M:%S GMT').strftime('%Y-%m-%dT%H:%M:%S.%f')

    def extract_market(self):
        return ccy.currency(self.currency).default_country

    def extract_name(self, response):
        return response.css('h1.name::text').get().strip()

    def extract_description(self, response):
        return [data.strip() for data in response.css('#description > p::text').getall()]

    def extract_care(self, response):
        return [c.strip() for c in response.css('#panCaracteristica > p::text').getall()]

    # def extract_image_urls(self, response):
    #     image_urls = response.css('.product-image-wrapper a::attr("href")').getall()
    #     return image_urls
    #
    # def extract_skus(self, response, price):
    #     product_data = ast.literal_eval(response.css('div.product-data-mine::attr("data-lookup")').get())
    #
    #     common_sku = {'price': price, 'currency': JackLemkusCrawler.currency}
    #     skus = []
    #     for data in product_data.values():
    #         sku = common_sku.copy()
    #         sku['size'] = data.get('size')
    #         sku['out_of_stock'] = not data['stock_status']
    #         sku['sku_id'] = data.get('id')
    #         skus.append(sku)
    #
    #     return skus

    def extract_price(self, response):
        return response.css('#lblPrecoPor > strong::text').get()

    def extract_crawl_start_time(self):
        return self.crawler.stats._stats['start_time'].strftime('%Y-%m-%dT%H:%M:%S.%f')


def check_words_existence(words, text):
    return any(word in text for word in words)

