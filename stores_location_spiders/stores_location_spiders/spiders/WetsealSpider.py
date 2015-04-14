import re
import urlparse

from scrapy.http import FormRequest
from scrapy.spider import Spider

from stores_location_spiders.items import StoresLocationSpidersItem
import helper


class WetsealSpider(Spider):
    name = 'wetseal_spider'
    start_urls = ['http://www.wetseal.com/Stores']

    def parse(self, response):
        states = response.xpath(
            ".//select[@id='dwfrm_storelocator_address_states_stateUSCA']//option[@value!='']/@value").extract()
        url = helper.get_text_from_node(response.xpath("//form[@id='dwfrm_storelocator_state']/@action"))
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
        item = StoresLocationSpidersItem()
        item['store_name'] = self.get_store_name(result)
        item['store_id'] = self.get_store_id(result)
        item['address'] = self.get_store_address(result)
        address_parts = self.parse_address(item['address'])
        item.update(address_parts)
        item['store_url'] = self.get_store_url(result, base_url)
        item['store_floor_plan_url'] = self.get_store_map_url(result)
        item['hours'] = self.get_store_hours(result)
        item['country'] = 'United States'
        return item

    def get_store_name(self, result):
        name = result.xpath(".//*[@class='store-name']//text()")
        return helper.get_text_from_node(name)

    def get_store_id(self, result):
        store_id = result.xpath('.//td[1]/a/@id')
        return helper.get_text_from_node(store_id)

    def get_store_address(self, result):
        address = result.xpath(".//*[@class='store-address']//text()").extract()
        if address:
            return [helper.normalize(x) for x in address]

    def parse_address(self, address):
        if len(address) == 3:
            address_parts = {}
            second_line_parts = address[1].split(',')  # parse 2nd line of address for city , state and zip
            address_parts['city'] = second_line_parts[0]
            address_parts['state'] = second_line_parts[1].split()[0]
            address_parts['zipcode'] = second_line_parts[1].split()[1]
            address_parts['phone_number'] = address[2]
            return address_parts

    def get_store_url(self, result, base_url):
        store_url = result.xpath('.//td[1]/a/@href').extract()
        if store_url:
            url_parts = urlparse.urlparse(base_url)
            return url_parts.scheme + "://" + url_parts.netloc + store_url[0]

    def get_store_map_url(self, result):
        map_url = result.xpath('//*[@class="store-map storelocator-results-link"]/a/@href').extract()
        if map_url:
            return map_url[0]

    def get_store_hours(self, result):
        lines = result.xpath(".//*[@class='store-hours']//text()").extract()
        return self.get_hours_dict(lines)

    def get_hours_dict(self, hour_rows):
        hours = {}
        for row in helper.normalize(hour_rows):
            day_string = helper.normalize(re.findall("[A-Za[A-Za-z]+ *- *[A-Za-z]+|[A-Za-z]+|.*", row)[0])
            hour_string = helper.normalize(row.replace(day_string, '').strip(':'))
            if hour_string and '-' not in hour_string:
                if 'Now' not in day_string:
                    hours[day_string.strip(':')] = {"status": hour_string}
            else:
                if ',' in day_string and hour_string:
                    # timing for consective days seperated by comma.
                    all_days = day_string.split(',')
                    open_time, close_time = hour_string.split('-')
                    for day in all_days:
                        hours[day.strip()] = {"open": open_time.strip(), "close": close_time.strip()}
                else:
                    open_time, close_time = hour_string.split('-')
                    hours[day_string.strip(':').strip(':')] = {"open": open_time.strip(),
                                                               "close": close_time.strip()}
        return hours
