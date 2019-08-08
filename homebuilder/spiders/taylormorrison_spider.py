import json
import re
import time

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule, Request

from ..items import HouseBuilder


class TaylormorrisonSpider(CrawlSpider):
    name = 'taylormorrison'
    builder = 'Taylor Morrison'

    allowed_domains = ['taylormorrison.com']
    start_urls = ['https://www.taylormorrison.com']

    house_details_css = '.plan-middle1 span::text'
    communities_css = ['.innerdivi']

    communitites_url = 'https://www.taylormorrison.com/services/SearchMethods.asmx/GetSearchResults'

    rules = [
        Rule(LinkExtractor(restrict_css=communities_css), callback='parse_states')
    ]

    def parse_states(self, response):
        search_url = response.css('#hndsearchPath::attr(value)').extract_first()

        headers = {
            'content-type': 'application/json; charset=UTF-8'
        }

        search_parameters = {
            "searchLocation": search_url,
            "sortBy": "1",
            "favorites": "",
            "isRealtor": "false",
            "isClearSession": "false",
            "isHTH": "false"
        }

        return Request(self.communitites_url, headers=headers, method='POST',
                       body=json.dumps(search_parameters), callback=self.extract_communities)

    def parse_communities(self, response):
        house_item = response.meta.get('house_item')
        house_item['url'] = response.url

        yield from self.extract_floor_plans(response)
        yield from self.extract_quick_move_in(response)

    def parse_homes(self, response):
        css = 'script:contains("PlanInitialData")::text, script:contains("var initialData")::text'
        script = response.css(css).extract_first()

        if not script:
            return

        products = re.findall(r",url:\s\'(.*?)\'", script, re.S)
        qmi_lot = re.findall(r"lot:\s\'(.*?)\'", script, re.S)

        if not qmi_lot:
            return [Request(response.urljoin(url), callback=self.parse_item, meta=response.meta.copy())
                    for url in products]

        home_requests = []
        for url, qmi in list(zip(products, qmi_lot)):
            meta = response.meta.copy()
            meta['house_item']['qmi_lot'] = qmi

            home_requests.append(Request(response.urljoin(url), callback=self.parse_item, meta=meta.copy()))

        return home_requests

    def parse_item(self, response):
        house_item = response.meta.get('house_item')

        if house_item['house_type'] == 'Quick Move In':
            house_item['qmi_address'] = self.extract_qmi_address(response)

        house_item['community_address'] = self.extract_address(response)
        house_item['builder'] = self.builder
        house_item['price'] = self.extract_price(response)
        house_item['hsf'] = self.extract_area(response)
        house_item['br'] = self.extract_bedrooms(response)
        house_item['ba'] = self.extract_baths(response)
        house_item['half_bath'] = self.extract_half_baths(response)
        house_item['ga'] = self.extract_garage(response)
        house_item['stories'] = self.extract_stories(response)
        house_item['model'] = self.extract_model(response)
        house_item['entry_date'] = time.strftime('%m/%d/%Y')

        return house_item

    def extract_communities(self, response):
        communitites_requests = []
        communities_info = json.loads(json.loads(response.text)['d'])['CommunityInfo']

        for community in communities_info:
            house_item = HouseBuilder()

            house_item['phone_number'] = community['Phone']
            house_item['city'] = community['City']
            house_item['zip_code'] = community['ZipPostalCode']
            house_item['latitude'] = community['CommunityLatitude']
            house_item['longitude'] = community['CommunityLongitude']
            house_item['state'] = community['StateProvince']
            house_item['community'] = community['Name']

            communitites_requests.append(Request(community['CommunityDetailsURL'],
                                                 callback=self.parse_communities,
                                                 meta={'house_item': house_item}))

        return communitites_requests

    def extract_floor_plans(self, response):
        house_item = response.meta.get('house_item').copy()
        house_item['house_type'] = 'Base Floor Plan'

        yield Request(response.urljoin(response.css('#floorPlans::attr(href)').extract_first()),
                      callback=self.parse_homes, meta={'house_item': house_item})

    def extract_quick_move_in(self, response):
        house_item = response.meta.get('house_item').copy()
        house_item['house_type'] = 'Quick Move In'

        yield Request(response.urljoin(response.css('#homeforsale::attr(href)').extract_first()),
                      callback=self.parse_homes, meta={'house_item': house_item})

    def extract_address(self, response):
        return response.css('.address span::text').extract_first().strip()

    def extract_qmi_address(self, response):
        return response.css('.plan-middle1 h1::text').extract_first().strip()

    def extract_price(self, response):
        price = self.extract_details(r'(\$\d+,*\d+)', response)
        return price[0] if price else ''

    def extract_area(self, response):
        return self.extract_details(r'(\d+,*\d+)\sSq. Ft.', response)[0]

    def extract_bedrooms(self, response):
        return int(self.extract_details(r'(\d+)\s+Bedrooms', response)[0])

    def extract_baths(self, response):
        return int(self.extract_details(r'(\d+)\s+Baths', response)[0])

    def extract_half_baths(self, response):
        half_baths = self.extract_details(r'(\d+)\s+Half Baths', response)
        return int(half_baths[0]) if half_baths else ''

    def extract_garage(self, response):
        return int(self.extract_details(r'(\d+)\s+Garage', response)[0])

    def extract_stories(self, response):
        return int(self.extract_details(r'(\d+)\s+(Stories|Story)', response)[0])

    def extract_model(self, response):
        return response.css('.breadcrumb li a::text').extract()[-2]

    def extract_details(self, regex, response):
        return response.css(self.house_details_css).re(regex)
