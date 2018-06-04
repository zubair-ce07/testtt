import os
import csv
import urllib.parse

from scrapy.http import Request
from scrapy.spiders import CrawlSpider
from scrapylab.items import FonectaItemLoader


class Fonecta(CrawlSpider):
    name = 'fonecta'
    allowed_domains = ['fonecta.fi']
    start_urls = ['https://www.fonecta.fi']
    start_urls_t = 'https://www.fonecta.fi/haku?what={}'
    categories = []

    def __init__(self):
        super(Fonecta).__init__()
        self.categories = self.read_file(
            # urllib.parse.urljoin('{}{}'.format(os.getcwd(), '/'), 'search-data/Categories_Generic.csv')
            urllib.parse.urljoin('{}{}'.format(os.getcwd(), '/'), 'search-data/Categories_Generic_test.csv')
        )

    def read_file(self, file_path):
        with open(file_path, "r") as file_content:
            csv.register_dialect('MyDialect', skipinitialspace=True)
            csv_reader = csv.DictReader(file_content, dialect='MyDialect')
            search_base = []

            for row in csv_reader:
                if 'postal' in file_path:
                    search_area = row["Province"]
                else:
                    search_area = row["Categories"]
                search_base.append(search_area)
            return search_base

    def parse(self, response):
        for category in self.categories:
            url = self.start_urls_t.format(category)
            request = Request(response.urljoin(url), callback=self.parse_urls)
            request.meta['search_category'] = category
            yield request

    def parse_urls(self, response):
        yield self.pagination(response)
        product_urls = response.css('.search-result-title a::attr(href)').extract()
        for url in product_urls:
            request = Request(response.urljoin(url), callback=self.parse_item)
            request.meta['search_category'] = response.meta.get('search_category')
            yield request

    def pagination(self, response):
        next_url = response.xpath('//*[@rel="next"]/@href').extract_first()
        request = Request(response.urljoin(next_url), callback=self.parse_urls)
        request.meta['search_category'] = response.meta.get('search_category')
        return request

    def parse_item(self, response):
        loader = FonectaItemLoader(response=response)

        loader.add_value('search_category', response.meta.get('search_category'))
        loader.add_value('url', response.url)
        loader.add_value('language', 'Finnish')
        loader.add_css('company_name', '.profile-heading-name-title::text')
        loader.add_css('telephone', '.phone-number-full::text')
        loader.add_css('address', '.address-link span::text')
        loader.add_xpath('postcode', '//*[@itemprop="postalCode"]/text()'),
        loader.add_css('website', '.website::text')
        loader.add_css('email','.email::text')
        loader.add_xpath('about_us', '//*[@id="company-description"]//text()')
        loader.add_css('brands', '#brands p::text')
        loader.add_css('categories', '.profile-supercategory-link-box a h4::text')

        item_businesses = response.xpath('//*[@class="customer-descriptions-item"]//text()').extract()
        loader.add_value('services', self.extract_business(item_businesses, ['services', 'Palvelut', 'Pyykkietikka']))
        loader.add_value('specialities', self.extract_business(item_businesses, ['Erikoistuminen']))
        loader.add_value('products', self.extract_business(item_businesses, ['Tuotteet', 'tuotteet']))
        yield loader.load_item()

    def extract_business(self, raw_business, business_type):
        for business in raw_business:
            for type in business_type:
                if type in business:
                    return raw_business
