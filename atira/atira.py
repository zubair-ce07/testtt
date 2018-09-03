import re
import datetime

import scrapy
from scrapy.spiders import CrawlSpider
from scrapy import Request, Selector


class Item(scrapy.Item):
    deals = scrapy.Field()
    property_name = scrapy.Field()
    landlord_slug = scrapy.Field()
    property_description = scrapy.Field()
    property_contact_info = scrapy.Field()
    property_amenities = scrapy.Field()
    property_images = scrapy.Field()
    room_photos = scrapy.Field()
    deposit_type = scrapy.Field()
    property_url = scrapy.Field()
    room_availability = scrapy.Field()
    room_amenities = scrapy.Field()
    floor_plans = scrapy.Field()
    listing_type = scrapy.Field()
    deposit_amount = scrapy.Field()
    deposit_name = scrapy.Field()
    property_ts_cs_url = scrapy.Field()
    room_name = scrapy.Field()
    room_price = scrapy.Field()
    min_duration = scrapy.Field()
    available_from = scrapy.Field()
    room_type = scrapy.Field()
    property_id = scrapy.Field()
    unit_id = scrapy.Field()
    pid = scrapy.Field()


class Atira(CrawlSpider):
    custom_settings = {}
    name = 'atira'
    land_lord_slug = 'atira-student-living'
    property_ts_cs_url = 'https://atira.com/terms-conditions/'
    home_url = 'https://atira.com/'
    start_urls = [
        'https://atira.com/why-atira/specials/'
    ]
    allowed_domains = ['atira.com']

    deals = []
    available_from = str(datetime.date.today())

    def parse(self, response):
        self.deals = response.css('.wrap.cf.two-column-padding p:first-of-type::text').extract()
        yield Request(url=self.home_url, callback=self.parse_atira)

    def parse_atira(self, response):
        item = Item()
        item['landlord_slug'] = self.land_lord_slug
        item['property_ts_cs_url'] = self.property_ts_cs_url
        item['deals'] = self.deals

        yield from self.make_locations_requests(response, item)

    def parse_location(self, response):
        if '/atira.com' in response.url:
            return self.parse_woolloongabba_south_brisbane(response)
        elif 'toowong' or 'waymouth' in response.url:
            return {}#self.parse_toowong_waymouth(response)
        return {}#self.parse_peel_latrobe(response)

    def parse_woolloongabba_south_brisbane(self, response):
        item = response.meta['item']

        item['property_name'] = 'atira ' + response.css('.flexslider-caption::text').extract_first().split(', ')[1]
        item['property_description'] = response.css('.entry-content ::text').extract()
        item['property_contact_info'] = self.extract_contact_info(response)

        yield from self.make_facilities_requests(response, item)

    def parse_toowong_waymouth(self, response):
        pass

    def parse_peel_latrobe(self, response):
        pass

    def parse_facilities(self, response):
        item = response.meta['item']
        reg = '\((.+)\)'
        item['property_images'] = sum([re.findall(reg, a) for a in response.css('.slides li::attr(style)').extract()], [])
        item['property_amenities'] = response.css('.home-icon-grid-contents p::text').extract()

        yield from self.make_apartment_requests(response.meta['urls'], item)

    def parse_rooms(self, response):
        item = response.meta['item']

        item['property_url'] = response.url
        item['floor_plans'] = response.css('.floorplan-thumbnail a::attr(data-featherlight)').extract()
        item['room_photos'] = response.css('.flexslider-roomtype li::attr(style)').extract()
        item['room_amenities'] = response.css('.home-icon-grid-inner-container p::text').extract()
        item['room_availability'] = self.detect_availability(response)
        item['available_from'] = self.available_from
        item['deposit_type'] = 'fixed'
        item['deposit_name'] = 'deposit'
        item['deposit_amount'] = ''
        item['listing_type'] = 'flexible_open_end'

        room_variants = self.extract_rooms_info(response)
        for room in room_variants:
            item_ = item.copy()
            item_.update(room)
            yield item_

    def make_locations_requests(self, response, item):
        location_urls = response.css('.location-three-col a::attr(href)').extract()
        location_requests = []
        for url in location_urls:
            request = Request(url=url, callback=self.parse_location)
            request.meta['item'] = item.copy()
            location_requests.append(request)
        return location_requests

    def make_facilities_requests(self, response, item):
        apartment_urls = response.css('.d-1of3 a::attr(href)').extract()
        facilities_url = response.css('.grid-seemore ::attr(href)').extract_first()
        facility_request = Request(url=facilities_url, callback=self.parse_facilities)
        facility_request.meta['item'] = item
        facility_request.meta['urls'] = apartment_urls
        return [facility_request]

    def make_apartment_requests(self, apartment_urls, item):
        css_2 = '#rooms .et_pb_module.et_pb_image > a::attr(href)'
        #apartment_urls = response.css('.d-1of3 a::attr(href)').extract()

        apartment_requests = []
        for url in apartment_urls:
            request = Request(url=url, callback=self.parse_rooms)
            request.meta['item'] = item.copy()
            apartment_requests.append(request)
        return apartment_requests

    def extract_rooms_info(self, response):
        apartment_name = response.css('.page-title ::text').extract_first()
        room_raw_names = [''.join(Selector(text=html).css('::text').extract())
                          for html in response.css('thead th').extract()[1:]]
        duration_and_prices = [Selector(text=html).css('::text').extract() for html in response.css('.row-hover tr').extract()]

        price_name_map = {}
        for duration_and_price in duration_and_prices:
            price_name_map[duration_and_price[0]] = zip(room_raw_names, duration_and_price[1:])
        rooms_info = []
        for semester, rooms in price_name_map.items():
            room_info = {'min_duration': semester}
            for room in rooms:
                room_info['room_name'] = apartment_name + room[0]
                room_info['room_price'] = room[1]
                rooms_info.append(room_info)
        return rooms_info

    def detect_availability(self, response):
        button_css = '.button-max::text'
        if response.css(button_css).extract_first() == 'Book Now':
            return 'Available'
        return 'Fully Booked'

    def extract_contact_info(self, response):
        return []
