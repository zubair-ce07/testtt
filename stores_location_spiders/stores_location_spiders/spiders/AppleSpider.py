import re
from urlparse import urljoin

from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request

from stores_location_spiders.items import StoresLocationSpidersItem
import helper


class AppleSpider(CrawlSpider):
    name = 'apple_spider'
    start_urls = ['http://www.apple.com/retail/storelist/']  # http://www.apple.com/retail/storelist/

    rules = ( Rule(
        SgmlLinkExtractor(
            restrict_xpaths=".//div[@class='listing']//a"),
        callback='parse_item'),)

    country_code_mappings = {"us": "United States",
                             "au": "Australia",
                             "br": "Brazil",
                             "ca": "Canada",
                             "cn": "China",
                             "fr": "France",
                             "de": "Germany",
                             "hk": "Hong Kong",
                             "it": "Italy",
                             "jp": "Japan",
                             "nl": "Netherlands",
                             "es": "Spain",
                             "se": "Sweden",
                             "tr": "Turkey",
                             "uk": "United Kingdom",
                             "chde": "swizerland"}


    def parse_item(self, response):
        item = StoresLocationSpidersItem()
        address_parts = self.get_address_parts(response)
        item.update(address_parts)
        item['country'] = self.get_country(response)
        if item['country'] in ['us', 'United States']:
            item['address'] = self.construct_address(address_parts, response)
        item['hours'] = self.get_hours(response, item["country"])
        item['store_name'] = self.get_store_name(response)
        item['store_url'] = response.url
        item['store_image_url'] = self.get_store_image_url(response)
        item['services'] = self.get_services(response)
        request_url = self.get_url(response)
        yield Request(url=request_url, meta={'item': item},
                      callback=self.parse_json)

    def parse_json(self, response):
        item = response.meta['item']
        map_url = re.findall('directions_link: "(.*)"', response.body)
        store_id = re.findall('store_number: "(.*)"', response.body)
        if item['country'] != 'United States':  # address of US is already fetched.
            address = re.findall('formatted_address: "(.*)"', response.body)
            if address:
                address_lines = address[0].split('<br />')
                item['address'] = address_lines
        if store_id:
            item['store_id'] = store_id[0]
        if map_url:
            item['store_floor_plan_url'] = map_url[0]
        return item

    def get_city(self, response):
        city = response.xpath(".//span[@class='locality']/text()")
        return helper.get_text_from_node(city)

    def get_country(self, response):
        for country_code, country_name in self.country_code_mappings.iteritems():
            if country_code in response.url.split('/'):
                return country_name
        # In case of US, the url does not contain country_code.
        return self.country_code_mappings["us"]

    def get_hours(self, response, country):
        if country == self.country_code_mappings["us"]:  # ' Only US stores hours are neccessary
            info_rows = response.xpath(".//table[@class='store-info']//tr[count(td)=2]")
            hours = dict()
            for row in info_rows:
                hours_data = helper.get_text_from_node(row.xpath('./td[2]/text()'))
                days = helper.get_text_from_node(row.xpath('./td[1]/text()'))
                if hours_data and '-' not in hours_data:
                    hours[days.strip(':')] = {"status": hours_data}
                else:
                    if ',' in days and hours_data:
                        # timing for consective days seperated by comma.
                        all_days = days.split(',')
                        open_time, close_time = hours_data.split('-')
                        for day in all_days:
                            hours[day.strip().strip(':')] = {"open": open_time.strip(), "close": close_time.strip()}
                    elif ':' not in days:
                        hours['Mon - Sat'] = {'status': days}
                    else:
                        open_time, close_time = hours_data.split('-')
                        hours[days.strip(':')] = {"open": open_time.strip(), "close": close_time.strip()}
            return hours

    def get_phone_number(self, response):
        phone_numbers = response.xpath(".//*[@class='telephone-number']//text()")
        return helper.get_text_from_node(phone_numbers)

    def get_state(self, response):
        states = response.xpath(".//*[@class='region']//text()")
        return helper.get_text_from_node(states)

    def get_store_name(self, response):
        store_name = response.xpath(".//*[@class='store-name']//text()")
        return helper.get_text_from_node(store_name)

    def get_zipcode(self, response):
        zip_codes = response.xpath(".//*[@class='postal-code']//text()")
        return helper.get_text_from_node(zip_codes)

    def get_store_image_url(self, response):
        image_urls = response.xpath(".//*[@class='store-summary']//img/@src").extract()
        if image_urls:
            return image_urls[0]

    def get_street_address(self, response):
        street_address = response.xpath(".//*[@class='street-address']//text()")
        return helper.get_text_from_node(street_address)

    def get_address_parts(self, response):
        address_parts = {}
        address_parts['city'] = self.get_city(response)
        address_parts['state'] = self.get_state(response)
        address_parts['zipcode'] = self.get_zipcode(response)
        address_parts['phone_number'] = self.get_phone_number(response)
        return address_parts

    def construct_address(self, address_parts, response):
        address = []
        address_parts['street_address'] = self.get_street_address(response)
        address.append(address_parts['street_address'])
        address.append(address_parts['city'] + ', ' + address_parts['state'] + ' ' + address_parts['zipcode'])
        return address

    def get_services(self, response):
        services = response.xpath(".//*[contains(@class,'hero-nav')]//a[contains(@class,'block')]//img/@alt").extract()
        if services:
            return [helper.normalize(x) for x in services]

    def get_url(self, response):
        url = response.xpath(".//script[contains(@src, 'maps_data.js')]/@src").extract()
        if url:
            return urljoin('http://www.apple.com/', url[0])
