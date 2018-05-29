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
            urllib.parse.urljoin('{}{}'.format(os.getcwd(), '/'), 'scrapylab/search-data/Categories_Generic.csv')
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
        item_json = raw_json.get('reduxAsyncConnect', {}).get('detailApi', {})
        item_detail = item_json.get('details', {})
        item_reviews = item_json.get('reviews', {})

        loader.add_value('url', response.url)
        loader.add_value('company_name', item_detail.get('name'))
        loader.add_value('telephone', item_detail.get('phone'))
        loader.add_value('address', self.extract_addr(item_detail.get('address')))
        loader.add_value('postcode', item_detail.get('address', {}).get('zipCode', {})),
        loader.add_value('city', item_detail.get('address', {}).get('city', {}).get('name', {})),
        # loader.add_value('latitude', item_detail.get('address', {}).get('coordinates', {}).get('latitude', {})),
        # loader.add_value('longitude', item_detail.get('address', {}).get('coordinates', {}).get('longitude', {})),
        loader.add_value('about_us', item_detail.get('businessDescription', {}).get('text', {}))
        loader.add_value('website', item_detail.get('website', {}).get('_link', {}))
        loader.add_value('email', item_detail.get('email', {}))

        item_businesses = item_json.get('onlineProfile', {}).get('hsppKeywords', [])
        loader.add_value('services', self.extract_business(item_businesses, 'Diensten'))
        loader.add_value('specialties', self.extract_business(item_businesses, 'Specialisatie'))
        # loader.add_xpath('products', xpath.format('Products and Services'))
        # loader.add_xpath('associations', xpath.format('Association'))
        if item_reviews.get('reviewProviders', []):
            loader.add_value('average_rating', self.extract_rating(item_reviews.get('reviewProviders', [])))
            loader.add_value('review_content', self.extract_reviews(item_reviews.get('detailedReviewItems', [])))

        loader.add_value('search_category', response.meta['search_category'])
        return loader.load_item()

    def extract_addr(self, address):
        return "{} {} {} {}".format(
            address.get('street', {}),
            address.get('houseNoFrom', {}),
            address.get('zipCode', {}),
            address.get('city', {}).get('name', {})
        )

    def extract_business(self, raw_business, business_type):
        for business in raw_business:
            if business.get('label', {}) == business_type:
                return business.get('values', {})

    def extract_rating(self, raw_rating):
        for rating in raw_rating:
            return "{}".format(rating.get('avgRating', {}))

    def extract_reviews(self, raw_reviews):
        reviews = []
        for raw_review in raw_reviews:
            reviews.append(raw_review.get('description', ''))
        return reviews

    def pagination(self, response):
        next_url = response.xpath('//*[a/text()="Volgende"]//@href').extract_first()
        request = Request(response.urljoin(next_url), callback=self.parse_urls)
        request.meta['search_category'] = response.meta['search_category']
        return request

