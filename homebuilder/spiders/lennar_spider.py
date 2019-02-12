import time
import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, Request, CrawlSpider

from ..items import HouseBuilder


class LennarCrawlSpider(CrawlSpider):
    name = 'lennar'
    builder = 'Lennar'
    allowed_domains = ['lennar.com']
    start_urls = ['https://www.lennar.com/find-a-home']

    homes_api_url = 'https://www.lennar.com/Services/Rest/SearchMethods.svc/Get{}TabDetails'

    community_attrs = {
        'pageState': {
            'ct': 'A',
            'sb': 'price',
            'pn': 1,
            'ps': 17,
            'ss': 0,
            'ic': 0,
            'so': 'asc',
            'attr': ''
        },
        'tabLocation': {
            'mi': '0',
            'lat': 0,
            'long': 0
        }
    }
    headers = {'Content-Type': 'application/json; charset=UTF-8'}

    community_css = ['.dyst-overflow']

    rules = [
        Rule(LinkExtractor(restrict_css=community_css), callback='parse')
    ]

    def parse(self, response):
        if not response.css('.divMenu'):    # Not community page
            return super().parse(response)

        return self.parse_community(response)

    def parse_community(self, response):
        item = HouseBuilder()
        item['builder'] = self.builder
        item['community'] = self.extract_community_name(response)
        item['community_address'] = self.extract_community_address(response)
        item['city'] = self.extract_city(response)
        item['state'] = self.extract_state(response)
        item['zip_code'] = self.extract_zip_code(response)
        item['latitude'] = self.extract_latitude(response)
        item['longitude'] = self.extract_longitude(response)
        item['url'] = response.url

        response.meta['item'] = item.copy()

        yield from [
            self.extract_floor_plans_request(response),
            self.extract_quick_move_ins_request(response)
        ]

    def parse_homes(self, response):
        item = response.meta['item']
        item['house_type'] = response.meta['house_type']
        item['entry_date'] = time.strftime('%m/%d/%Y')

        raw_homes = json.loads(response.text)

        for raw_home in raw_homes.get('pr') or raw_homes.get('ir', []):
            home_item = item.copy()
            home_item['phone_number'] = raw_home['php']
            home_item['model'] = raw_home['plmktnm']
            home_item['price'] = raw_home['price']
            home_item['hsf'] = raw_home['sgft']
            home_item['stories'] = raw_home['story']
            home_item['br'] = int(raw_home['bedrm'])
            home_item['ba'] = float(raw_home['bathrm'].replace('+', ''))
            home_item['half_bath'] = int(raw_home['hlfbathrm'])
            home_item['ga'] = int(raw_home['gagebay'])

            if home_item['house_type'] == 'Quick Move In':
                home_item['qmi_address'] = raw_home['spdAdd']
                home_item['qmi_lot'] = raw_home['lId']

            yield home_item

    def extract_floor_plans_request(self, response):
        meta = response.meta.copy()
        meta['house_type'] = 'Base Floor Plan'

        body = self.community_attrs.copy()
        body['CommunityID'] = self.extract_community_id(response)
        body['pageState']['ad'] = True

        request_url = self.homes_api_url.format('Homes')

        return Request(url=request_url, method='POST', callback=self.parse_homes,
                       meta=meta.copy(), body=json.dumps(body), headers=self.headers)

    def extract_quick_move_ins_request(self, response):
        meta = response.meta.copy()
        meta['house_type'] = 'Quick Move In'

        body = self.community_attrs.copy()
        body['CommunityID'] = self.extract_community_id(response)
        body['pageState']['pt'] = '\u0000'
        body['pageState']['ius'] = False

        request_url = self.homes_api_url.format('Inventory')

        return Request(url=request_url, method='POST', callback=self.parse_homes,
                       meta=meta.copy(), body=json.dumps(body), headers=self.headers)

    def extract_community_name(self, response):
        return response.css('[name="Community Name"]::attr(content)').extract_first()

    def extract_city(self, response):
        return response.css('[property="og:locality"]::attr(content)').extract_first()

    def extract_state(self, response):
        return response.css('[name="State"]::attr(content)').extract_first()

    def extract_zip_code(self, response):
        return int(response.css('.hdnCommunityZip::attr(value)').extract_first())

    def extract_raw_address(self, response):
        return response.css('script:contains("var latitude")')

    def extract_latitude(self, response):
        return self.extract_raw_address(response).re_first('var latitude = parseFloat\(\'(.*?)\'\);')

    def extract_longitude(self, response):
        return self.extract_raw_address(response).re_first('var longitude = parseFloat\(\'(.*?)\'\);')

    def extract_community_address(self, response):
        return self.extract_raw_address(response).re_first('var CommunityAddress = "(.*?),')

    def extract_community_id(self, response):
        return response.css('.hdnCommunityID::attr(value)').extract_first()
