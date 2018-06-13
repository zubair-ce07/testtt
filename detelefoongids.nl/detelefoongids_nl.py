import os
import csv
import json
import urllib.parse

from scrapy.http import Request
from scrapy.spiders import CrawlSpider
from scrapylab.items import DeteleFoongidsItemLoader


class DeteleFoongids(CrawlSpider):
    name = 'detelefoongids'
    allowed_domains = ['detelefoongids.nl']
    start_urls = ['https://www.detelefoongids.nl']
    start_urls_t = ['https://www.detelefoongids.nl/{}/4-1/']
    categories = []

    def __init__(self):
        super().__init__()
        self.categories = self.read_file(
            urllib.parse.urljoin('{}{}'.format(os.getcwd(), '/'), 'search-data/Categories_Generic.csv')
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
            url = self.start_urls_t[0].format(category)
            request = Request(response.urljoin(url), callback=self.parse_urls)
            request.meta['search_category'] = category
            yield request

    def parse_urls(self, response):
        yield self.pagination(response)
        product_urls = response.css('.resultItem h2 a::attr(href)').extract()
        for url in product_urls:
            request = Request(response.urljoin(url), callback=self.parse_item)
            request.meta['search_category'] = response.meta['search_category']
            yield request

    def parse_item(self, response):
        loader = DeteleFoongidsItemLoader(response=response)

        raw_json = json.loads(response.xpath('//script[contains(text(),"window.__data")]').
                              re("window.__data=(.*);")[0])
        item_json = raw_json.get('reduxAsyncConnect', {}).get('detailApi')

        item_detail = item_json.get('details', {})
        item_reviews = item_json.get('reviews', {})

        loader.add_value('search_category', response.meta.get('search_category'))
        loader.add_value('url', response.url)
        loader.add_value('company_name', item_detail.get('name'))
        loader.add_value('telephone', item_detail.get('phone'))
        loader.add_value('address', self.extract_addr(item_detail.get('address')))
        loader.add_value('postcode', item_detail.get('address', {}).get('zipCode')),
        loader.add_value('city', item_detail.get('address', {}).get('city', {}).get('name')),
        loader.add_value('website', item_detail.get('website', {}).get('_link'))
        loader.add_value('email', item_detail.get('email'))

        if item_detail.get('businessDescription'):
            loader.add_value('about_us', item_detail.get('businessDescription', {}).get('text'))

        item_businesses = item_json.get('onlineProfile', {}).get('hsppKeywords', [])
        loader.add_value('services', self.extract_business(item_businesses, ['Diensten']))
        loader.add_value('specialties', self.extract_business(item_businesses, ['Specialisatie', 'Specialiteiten']))
        loader.add_value('products', self.extract_business(item_businesses, ['Producten']))

        certifications = item_json.get('onlineProfile', {}).get('widgetAangesloten')
        loader.add_value('certifications', self.extract_certifications(certifications, 'Certificering'))

        if item_reviews.get('reviewProviders'):
            loader.add_value('average_rating', self.extract_rating(item_reviews.get('reviewProviders')))
            loader.add_value('review_content', self.extract_reviews(item_reviews.get('detailedReviewItems')))

        return loader.load_item()

    def extract_certifications(self, raw_business, cert_type):
        certs = []
        if raw_business.get('title'):
            if cert_type in raw_business.get('title'):
                for business in raw_business.get('details'):
                    certs.append("{}: {}".format(business.get('label')," ".join(business.get('values'))))
                return certs

    def extract_addr(self, address):
        return "{} {} {} {}".format(
            address.get('street', {}),
            address.get('houseNoFrom', {}),
            address.get('zipCode', {}),
            address.get('city', {}).get('name', {})
        )

    def extract_business(self, raw_business, business_type):
        for business in raw_business:
            for type in business_type:
                if business.get('label') == type:
                    return business.get('values')

    def extract_rating(self, raw_rating):
        for rating in raw_rating:
            return "{}".format(rating.get('avgRating'))

    def extract_reviews(self, raw_reviews):
        reviews = []
        for raw_review in raw_reviews:
            reviews.append(raw_review.get('description'))
        return reviews

    def pagination(self, response):
        next_url = response.xpath('//*[a/text()="Volgende"]//@href').extract_first()
        request = Request(response.urljoin(next_url), callback=self.parse_urls)
        request.meta['search_category'] = response.meta['search_category']
        return request

