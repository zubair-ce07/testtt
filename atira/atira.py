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


class Atira(CrawlSpider):
    custom_settings = {
        "DOWNLOAD_DELAY": 1
    }

    name = 'atira'
    land_lord_slug = 'atira-student-living'
    property_ts_cs_url = 'https://atira.com/terms-conditions/'
    home_url = 'https://atira.com/'
    available_date = str(datetime.date.today())

    start_urls = [
        'https://atira.com/why-atira/specials/'
    ]
    allowed_domains = ['atira.com']

    deals = []
    duration_map = {
        "1": '119',
        "2": '308'
    }
    name_map = (
        ('woolloongabba', 'Atira Woolloongabba'),
        ('south-brisbane', 'South Brisbane'),
        ('toowong', 'Toowong'),
        ('waymouth', 'Adelaide'),
    )

    def parse(self, response):
        self.deals = self.extract_deals(response)
        yield Request(url=self.home_url, callback=self.parse_atira)

    def parse_atira(self, response):
        item = Item()
        item['landlord_slug'] = self.land_lord_slug
        item['property_ts_cs_url'] = self.property_ts_cs_url
        item['deals'] = self.deals

        yield from self.make_locations_requests(response, item)

    def parse_location(self, response):
        if 'peel' in response.url or 'latrobe' in response.url:
            return self.parse_coming_soon(response)
        return self.parse_available_locations(response)

    def parse_available_locations(self, response):
        item = response.meta['item']

        item['property_name'] = self.extract_property_name(response)
        item['property_description'] = self.extract_property_description(response)
        item['property_contact_info'] = self.extract_contact_info(response)
        item['property_images'] = self.extract_property_images(response)
        item['property_amenities'] = self.extract_property_amenities(response)

        if self.has_facilities_url(response):
            yield from self.make_facilities_requests(response, item)
        else:
            yield from self.make_apartment_requests(self.extract_apartment_urls(response), item)

    def parse_coming_soon(self, response):
        yield {"Coming": "Soon"}

    def parse_facilities(self, response):
        item = response.meta['item']

        item['property_images'] = self.extract_property_images(response)
        item['property_amenities'] = self.extract_property_amenities(response)

        yield from self.make_apartment_requests(response.meta['urls'], item)

    def parse_rooms(self, response):
        item = response.meta['item']

        item['property_url'] = response.url
        item['floor_plans'] = self.extract_floor_plan(response)
        item['room_photos'] = self.extract_room_photos(response)
        item['room_amenities'] = self.extract_room_amenities(response)
        item['room_availability'] = self.detect_availability(response)
        item['available_from'] = self.available_date
        item['deposit_type'] = 'fixed'
        item['deposit_name'] = 'deposit'
        item['deposit_amount'] = ''
        item['listing_type'] = 'flexible_open_end'

        room_variants = self.extract_room_variants(response)
        for room in room_variants:
            copy_item = item.copy()
            copy_item.update(room)
            yield copy_item

    def make_locations_requests(self, response, item):
        location_urls = response.css('.location-three-col a::attr(href)').extract()

        location_requests = []
        for url in location_urls:
            request = Request(url=url, callback=self.parse_location)
            request.meta['item'] = item.copy()
            location_requests.append(request)
        return location_requests

    def make_facilities_requests(self, response, item):
        apartment_urls = self.extract_apartment_urls(response)

        facilities_url = response.css('.grid-seemore ::attr(href)').extract_first()
        facility_request = Request(url=facilities_url, callback=self.parse_facilities)
        facility_request.meta['item'] = item
        facility_request.meta['urls'] = apartment_urls

        return [facility_request]

    def make_apartment_requests(self, apartment_urls, item):
        apartment_requests = []
        for url in apartment_urls:
            request = Request(url=url, callback=self.parse_rooms)
            request.meta['item'] = item.copy()
            apartment_requests.append(request)
        return apartment_requests

    def has_facilities_url(self, response):
        return response.css('.grid-seemore ::attr(href)').extract_first()

    def extract_apartment_urls(self, response):
        css = '.d-1of3 a::attr(href), #rooms .et_pb_module.et_pb_image > a::attr(href)'
        return response.css(css).extract()

    def extract_room_variants(self, response):
        if self.has_no_table(response):
            return self.extract_no_table_room_info(response)

        apartment_name = response.css('.page-title ::text').extract_first()
        room_altitude = [''.join(Selector(text=html).css('::text').extract())
                         for html in response.css('thead th').extract()]
        room_altitude = [ra.strip() for ra in room_altitude if ra.strip()]
        duration_and_prices = [Selector(text=html).css('::text').extract()
                               for html in response.css('.row-hover tr').extract()]

        name_duration_prices = {}
        for row in duration_and_prices:
            if len(row) == len(room_altitude) + 2:
                apartment_name = row[0]
                name_duration_prices[apartment_name] = [row[1:]]
            else:
                if apartment_name in name_duration_prices.keys():
                    name_duration_prices[apartment_name] += [row]
                else:
                    name_duration_prices[apartment_name] = [row]

        rooms_info = []
        for apartment_name, duration_and_prices in name_duration_prices.items():
            for duration_and_price in duration_and_prices:
                for altitude, price in zip(room_altitude, duration_and_price[1:]):
                    room_info = {
                        'min_duration': self.duration_map.get(duration_and_price[0].split(' ')[0]),
                        'room_name': f'{apartment_name} {altitude}',
                        'room_price': price.split(' ')[0]
                    }
                    rooms_info.append(room_info)
        return rooms_info

    def extract_no_table_room_info(self, response):
        apartment_name = self.extract_apartment_name(response)
        prices = response.css('.room-type-pricebreakdown ::text').extract()

        regex = '(\d+).*?(\$\d+)'
        rooms_info = []
        for price in prices:
            duration, price = re.findall(regex, price)[0]
            room_info = {
                "min_duration": self.duration_map.get(duration),
                "room_name": apartment_name,
                "room_price": price,
            }
            rooms_info.append(room_info)

        return rooms_info

    def has_no_table(self, response):
        return not response.css('thead th').extract()

    def detect_availability(self, response):
        button_css = '.button-max::text'
        if response.css(button_css).extract_first() == 'Book Now':
            return 'Available'
        return 'Fully Booked'

    def extract_contact_info(self, response):
        reg = re.compile('.*#uber-google-map.*', re.S)
        script = response.css('script::text').re_first(reg) or ''

        contact_info_regex = re.compile(
            r"subtitle\":\"([^\"]+?)\"[^}]*?\"phone\":\"([^\"]+?)\"[^}]*?email\":\"(.*?)\""
        )
        raw_contact_info = contact_info_regex.findall(script)

        for contact_info in raw_contact_info:
            if contact_info[0] in self.extract_property_name(response):
                return list(contact_info[1:])
        return []

    def extract_room_photos(self, response):
        reg = '\((.+)\)'
        return sum([re.findall(reg, a) for a in response.css('.flexslider-roomtype li::attr(style)').extract()], [])

    def extract_property_images(self, response):
        property_images = response.css('.et_pb_lightbox_image::attr(href)').extract()

        reg = '\((.+)\)'
        return sum([re.findall(reg, a) for a in response.css('.slides li::attr(style)').extract()], property_images)

    def extract_floor_plan(self, response):
        return response.css('.floorplan-thumbnail a::attr(data-featherlight)').extract()

    def extract_room_amenities(self, response):
        return response.css('.home-icon-grid-inner-container p::text').extract()

    def extract_property_amenities(self, response):
        amenities = set([d.strip() for d in response.css('#facilities .et_pb_blurb_description ::text').extract()])
        return response.css('.home-icon-grid-contents p::text').extract() + list(amenities)

    def extract_property_name(self, response):
        for name_str, name in self.name_map:
            if name_str in response.url:
                return name

    def extract_property_description(self, response):
        description = list(set(response.css('.et_pb_fullwidth_header_subhead::text').extract()))
        return response.css('[itemprop="articleBody"] ::text').extract() + description

    def extract_apartment_name(self, response):
        return response.css('.page-title ::text').extract_first()

    def extract_deals(self, response):
        return response.css('.wrap.cf.two-column-padding p:first-of-type::text').extract()
