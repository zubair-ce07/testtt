import re
from urlparse import urljoin

from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule
from scrapy.http import Request
from scrapinghub.spider import BaseSpider
from stores_location_spiders.items import StoresLocationItem


class AppleSpider(BaseSpider):
    name = 'apple_spider'
    start_urls = ['http://www.apple.com/retail/storelist/']  # http://www.apple.com/retail/storelist/

    rules = ( Rule(
        SgmlLinkExtractor(
            restrict_xpaths=".//div[@class='listing']//a"),
        callback='parse_item'),)

    def parse_item(self, response):
        item = StoresLocationItem()
        address_parts = self.parse_address_parts(response)
        item.update(address_parts)
        item['country'] = self.store_country(response)
        if item['country'] == 'US':
            item['address'] = self.construct_address(address_parts, response)
        item['hours'] = self.store_hours(response, item["country"])
        item['store_name'] = self.store_name(response)
        item['store_url'] = response.url
        item['store_image_url'] = self.store_image_url(response)
        item['services'] = self.store_services(response)
        request_url = self.store_info_script_url(response)
        yield Request(url=request_url, meta={'item': item},
                      callback=self.parse_json)

    def parse_json(self, response):
        item = response.meta['item']
        store_id = re.findall('store_number: "(.*)"', response.body)
        if item['country'] != 'US':  # address of US is already fetched.
            address = re.findall('formatted_address: "(.*)"', response.body)
            if address:
                address_lines = address[0].split('<br />')
                item['address'] = self.normalize(address_lines)
        if store_id:
            item['store_id'] = store_id[0]
        return item

    def store_city(self, response):
        city = response.xpath("(.//span[@class='locality']/text())[1]")
        return self.get_text_from_node(city)

    def store_country(self, response):
        country = re.search('www.apple.com/([A-z]+)(/[A-z]+)?/retail', response.url)
        if country:
            return country.group(1).upper()
        # In case of US, the url does not contain country_code.
        return 'US'

    def store_hours(self, response, country):
        if country == "US":  # ' Only US stores hours are neccessary
            info_rows = response.xpath(".//table[@class='store-info']//tr[count(td)=2]")
            hours = dict()
            for row in info_rows:
                hours_data = self.get_text_from_node(row.xpath('./td[2]/text()'))
                days = self.get_text_from_node(row.xpath('./td[1]/text()'))
                if hours_data and '-' in hours_data:
                    open_time, close_time = [s.strip() for s in hours_data.split('-')]
                    if ',' in days:
                        # timing for consective days seperated by comma.
                        all_days = days.split(',')
                        for day in all_days:
                            hours[day.strip().strip(':')] = {"open": open_time, "close": close_time}
                    else:
                        if '-' in days:
                            hour_timings = {"open": open_time, "close": close_time}
                        # To parse and assign timing of open and close of store
                        # This method parse days of week between given interval of days on website
                            self.parse_store_hours(days.strip(':'), hour_timings, hours, True)
                        else:
                            hours[days.strip(':')] = {"open": open_time, "close": close_time}
                elif ':' not in days:
                    # To parse and assign timing of open and close of store
                    # when store timing is 24/7, 365 days a year
                    hour_timings = {'open': '00:00 am', 'close': '00:00 pm'}
                    self.parse_store_hours('Mon - Sun', hour_timings, hours, True)
            return hours

    def store_phone_number(self, response):
        phone_numbers = response.xpath("(.//*[@class='telephone-number']//text())[1]")
        return self.get_text_from_node(phone_numbers)

    def store_state(self, response):
        states = response.xpath("(.//*[@class='region']/text())[1]")
        return self.get_text_from_node(states)

    def store_name(self, response):
        store_name = response.xpath("(.//*[@class='store-name']//text())[1]")
        return self.get_text_from_node(store_name)

    def store_zipcode(self, response):
        zip_codes = response.xpath("(.//*[@class='postal-code']//text())[1]")
        return self.get_text_from_node(zip_codes)

    def store_image_url(self, response):
        image_urls = response.xpath(".//*[@class='store-summary']//img/@src").extract()
        if image_urls:
            return image_urls[0]

    def store_street_address(self, response):
        street_address = response.xpath("(.//*[@class='street-address']//text())[1]")
        return self.get_text_from_node(street_address)

    def parse_address_parts(self, response):
        address_parts = {}
        address_parts['city'] = self.store_city(response)
        address_parts['state'] = self.store_state(response)
        address_parts['zipcode'] = self.store_zipcode(response)
        address_parts['phone_number'] = self.store_phone_number(response)
        return address_parts

    def construct_address(self, address_parts, response):
        address = []
        address_parts['street_address'] = self.store_street_address(response)
        address.append(address_parts['street_address'])
        address.append("%s,%s %s" % (address_parts['city'], address_parts['state'], address_parts['zipcode']))
        return address

    def store_services(self, response):
        services = response.xpath(".//*[contains(@class,'hero-nav')]//a[contains(@class,'block')]//img/@alt").extract()
        return [self.normalize(x) for x in services]

    def store_info_script_url(self, response):
        url = response.xpath(".//script[contains(@src, 'maps_data.js')]/@src").extract()
        if url:
            return urljoin('http://www.apple.com/', url[0])
