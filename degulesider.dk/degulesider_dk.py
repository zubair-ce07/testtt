import os
import csv
import json
import urllib.parse

from scrapy.http import Request
from urllib.parse import urlencode
from scrapy.spiders import CrawlSpider
from scrapylab.items import degulesiderItemLoader


class DeguleSider(CrawlSpider):
    name = 'degulesider'
    allowed_domains = ['degulesider.dk']
    start_urls = ['https://www.degulesider.dk']

    def parse(self, response):
        categories = self.read_file(
            # urllib.parse.urljoin('{}{}'.format(os.getcwd(), '/'), 'search-data/Categories_Generic.csv')
            urllib.parse.urljoin('{}{}'.format(os.getcwd(), '/'), 'search-data/Categories_Generic_test.csv')
        )

        for category in categories:
            params = {
                "query": category,
                "profile": "dgs",
            }
            url = "{}/api/search/count?{}".format(response.url, urlencode(params))
            request = Request(url, callback=self.parse_pagination)
            request.meta['search_category'] = category
            yield request

    def read_file(self, file_path):
        with open(file_path, "r") as file_content:
            csv.register_dialect('MyDialect', skipinitialspace=True)
            csv_reader = csv.DictReader(file_content, dialect='MyDialect')
            search_base = []

            for row in csv_reader:
                search_area = row["Categories"]
                search_base.append(search_area)

            return search_base

    def parse_pagination(self, response):
        json_count = json.loads(response.text)
        for index in range(1, int(json_count['cs']/25) + 2):
            params = {
                "query": response.meta['search_category'],
                "profile": "dgs",
                "page": index
            }
            url = "{}/api/cs?{}".format(response.url[:-46], urlencode(params))
            request = Request(url, callback=self.parse_item_urls)
            request.meta['search_category'] = response.meta['search_category']
            yield request

    def parse_item_urls(self, response):
        json_list = json.loads(response.text)
        for item in json_list['items']:
            item_id = item['id']
            item_params = {
                "profile": "dgs"
            }
            url = response.url[:response.url.find('?')]
            item_url = "{}/{}?{}".format(url, item_id, urlencode(item_params))
            request = Request(item_url, callback=self.parse_item)
            request.meta['search_category'] = response.meta['search_category']
            yield request

    def parse_item(self, response):
        item = json.loads(response.text)
        loader = degulesiderItemLoader(response=response)
        loader.add_value('url', response.url)
        loader.add_value('company_name', item.get('name'))
        loader.add_value('country', item.get('nativeDistricts').get('country'))
        loader.add_value('telephone', self.number(item))
        loader.add_value('address', self.address(item))
        loader.add_value('postcode', self.postal_code(item))
        loader.add_value('about_us', item.get('companyDescription'))

        # Need some validation
        loader.add_value('email', item.get('contact').get('email').get('link'))

        # need some validation
        loader.add_value('website', item.get('contact').get('homepage').get('link'))

        loader.add_value('services', self.business_detail(item, ['Vi udfører', 'Ydelser']))
        loader.add_value('categories', self.category(item))
        loader.add_value('products', self.business_detail(item, ['Produkter']))
        loader.add_value('search_category', response.meta['search_category'])

        return loader.load_item()

    def number(self, item):
        return [num.get('phoneNumber') for num in item.get('phoneNumbers')]

    def address(self, item):
        for addr in item.get('address'):
            return "{} {} {} {}".format(
                addr.get('streetName'),
                addr.get('streetNumber'),
                addr.get('postCode'),
                addr.get('postArea')
            )

    def postal_code(self, item):
        return [addr.get('postCode') for addr in item.get('address')]

    def business_detail(self, item , business):
        for itm in item.get('freeText'):
            return [itm.get('text') for bus in business if itm.get('title') == bus]

    def category(self, item):
        return [itm.get('label') for itm in item.get('headings')]
