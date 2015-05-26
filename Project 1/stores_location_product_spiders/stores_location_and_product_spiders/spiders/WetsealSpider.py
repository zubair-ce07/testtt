import re
import urlparse

from scrapy.http import FormRequest
from stores_location_and_product_spiders.items import StoresLocationItem
from scrapinghub.spider import BaseSpider

class WetsealSpider(BaseSpider):
    name = 'wetseal_spider'
    start_urls = ['http://www.wetseal.com/Stores']

    def parse(self, response):
        states = response.xpath(
            ".//select[@id='dwfrm_storelocator_address_states_stateUSCA']//option[@value!='']/@value").extract()
        url = self.get_text_from_node(response.xpath("//form[@id='dwfrm_storelocator_state']/@action"))
        for state in states:
            form_data = {'dwfrm_storelocator_address_states_stateUSCA': state,
                         "dwfrm_storelocator_findbystate": "Search"}
            yield FormRequest(url,
                              formdata=form_data,
                              callback=self.parse_result_table)

    def parse_result_table(self, response):
        results_table = response.xpath(".//table[@id='store-location-results']//tbody/tr")
        for result in results_table:
            yield self.parse_item(result, response.url)

    def parse_item(self, result, base_url):
        item = StoresLocationItem()
        item['store_name'] = self.store_name(result)
        item['store_id'] = self.store_id(result)
        address_parts = self.parse_address(self.store_address(result))
        item.update(address_parts)
        item['store_url'] = self.store_url(result, base_url)
        item['hours'] = self.store_hours(result)
        item['country'] = 'United States'
        return item

    def store_name(self, result):
        return self.get_text_from_node(result.xpath(".//*[@class='store-name']//text()"))

    def store_id(self, result):
        return self.get_text_from_node(result.xpath('.//td[1]/a/@id'))

    def store_address(self, result):
        address = result.xpath(".//*[@class='store-address']//text()").extract()
        return self.normalize(address)

    def parse_address(self, complete_address):
        """
        Address block contains city, state, zipcode, street address and phone number information
        this method is used to populate these fields after parsing address block
        """
        address_parts = {}
        address = []
        address.append(complete_address[0])
        if len(complete_address) == 3:
            address_parts['phone_number'] = complete_address[2]
        second_line_parts = complete_address[1].split(',')  # parse 2nd line of address for city , state and zip
        address_parts['city'] = second_line_parts[0]
        state_zip = second_line_parts[1].split()
        address_parts['state'] = state_zip[0]
        address_parts['zipcode'] = state_zip[1]
        address_parts['address'] = address
        return address_parts

    def store_url(self, result, base_url):
        store_url = result.xpath('.//td[1]/a/@href').extract()
        if store_url:
            return urlparse.urljoin(base_url, store_url[0])

    def store_hours(self, result):
        lines = result.xpath(".//*[@class='store-hours']//text()").extract()
        return self.parse_hours(lines)

    def parse_hours(self, hour_rows):
        """
        Create day time dict from timings available on the website
        """
        hours = dict()
        for row in self.normalize(hour_rows):
            day_string = self.normalize(re.findall("^[A-z]+\s*-?\s*[A-z]+", row)[0]).strip(':')
            hour_string = self.normalize(row.replace(day_string, '').strip(':'))
            if hour_string and '-' in hour_string:
                open_time, close_time = self.normalize(hour_string.split('-'))
                hour_timings = {"open": open_time, "close": close_time}
                if ',' in day_string:
                    # timing for consecutive days separated by comma.
                    all_days = day_string.split(',')
                    for day in all_days:
                        hours[day.strip()] = hour_timings
                else:
                    if '-' in day_string:
                        # This method parse days of week between given interval of days on website
                        self.parse_store_hours(day_string.strip(':'), hour_timings, hours)
                    else:
                        hours[day_string.strip(':')] = hour_timings
        return hours

