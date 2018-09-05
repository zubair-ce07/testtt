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
    peel_latrobe_date = '2019-01-14'

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
        ('peel', 'Peel'),
        ('latrobe', 'La Trobe')
    )

    images_regex = re.compile('\((.+)\)')
    duration_price_regex = re.compile('(\d+).*?(\$\d+)')
    contact_info_regex = re.compile(
        r"subtitle\":\"([^\"]+?)\"[^}]*?\"phone\":\"([^\"]+?)\"[^}]*?email\":\"(.*?)\""
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
        item = response.meta['item']

        item['property_name'] = self.extract_property_name(response)
        item['property_description'] = self.extract_property_description(response)
        item['property_contact_info'] = self.extract_contact_info(response)
        item['property_images'] = self.extract_property_images(response)
        item['property_amenities'] = self.extract_property_amenities(response)

        if 'peel' in response.url or 'latrobe' in response.url:
            return self.parse_peel_latrobe(response, item)

        return self.parse_available_locations(response, item)

    def parse_available_locations(self, response, item):
        if self.has_facilities_link(response):
            yield from self.make_facilities_requests(response, item)
        else:
            yield from self.make_apartment_requests(self.extract_apartment_urls(response), item)

    def parse_peel_latrobe(self, response, item):
        item['property_url'] = response.url
        item['room_photos'] = []
        item['deposit_type'] = 'fixed'
        item['deposit_name'] = 'deposit'
        item['deposit_amount'] = ''
        item['listing_type'] = 'flexible_open_end'
        item['available_from'] = self.peel_latrobe_date

        rooms_css = '#rooms .et_pb_row_7 .et_pb_column, #rooms .et_pb_row_8 .et_pb_column :not(.et_pb_column_empty), ' \
                    '#rooms .et_pb_row_9 .et_pb_column'
        for apartment_html in response.css(rooms_css).extract():
            yield from self.extract_apartments_peel_latrobe(apartment_html, item.copy())

    def parse_facilities(self, response):
        item = response.meta['item']

        item['property_images'] = self.extract_property_images(response)
        item['property_amenities'] = self.extract_property_amenities(response)

        yield from self.make_apartment_requests(response.meta['urls'], item)

    def parse_apartments(self, response):
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

        return self.yield_variants(item, self.extract_room_variants(response))

    def extract_apartments_peel_latrobe(self, html, item):
        selector = Selector(text=html)

        item['room_photos'] = self.extract_room_photos(selector)
        item['room_amenities'] = self.extract_room_amenities(selector)
        item['room_availability'] = self.detect_availability(selector)
        item['floor_plans'] = self.extract_floor_plan(selector)

        return self.yield_variants(item, self.extract_peel_latrobe_room_variants(selector))

    def yield_variants(self, item, room_variants):
        for room in room_variants:
            copy_item = item.copy()
            copy_item.update(room)
            yield copy_item

    def make_locations_requests(self, response, item):
        css = '.location-three-col a::attr(href)'
        location_urls = response.css(css).extract()

        location_requests = []
        for url in location_urls:
            request = Request(url=url, callback=self.parse_location)
            request.meta['item'] = item.copy()
            location_requests.append(request)
        return location_requests

    def make_facilities_requests(self, response, item):
        apartment_urls = self.extract_apartment_urls(response)

        css = '.grid-seemore ::attr(href)'
        facilities_url = response.css(css).extract_first()
        facility_request = Request(url=facilities_url, callback=self.parse_facilities)
        facility_request.meta['item'] = item
        facility_request.meta['urls'] = apartment_urls

        return [facility_request]

    def make_apartment_requests(self, apartment_urls, item):
        apartment_requests = []
        for url in apartment_urls:
            request = Request(url=url, callback=self.parse_apartments)
            request.meta['item'] = item.copy()
            apartment_requests.append(request)
        return apartment_requests

    def has_facilities_link(self, response):
        css = '.grid-seemore ::attr(href)'
        return response.css(css).extract_first()

    def extract_apartment_urls(self, response):
        css = '.d-1of3 a::attr(href), #rooms .et_pb_module.et_pb_image > a::attr(href)'
        return response.css(css).extract()

    def extract_room_variants(self, response):
        if self.has_no_table(response):
            return self.extract_without_table_room_variants(response)

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

        rooms_variants = []
        for apartment_name, duration_and_prices in name_duration_prices.items():
            for duration_and_price in duration_and_prices:
                for altitude, price in zip(room_altitude, duration_and_price[1:]):
                    room_info = {
                        'min_duration': self.duration_map.get(duration_and_price[0].split(' ')[0]),
                        'room_name': f'{apartment_name} {altitude}',
                        'room_price': price.split(' ')[0]
                    }
                    rooms_variants.append(room_info)
        return rooms_variants

    def extract_peel_latrobe_room_variants(self, selector):
        apartment_name = self.extract_apartment_name(selector)
        html = selector.css('tr').extract()

        room_info_table = []
        for row in html:
            room_info_table.append([a.strip() for a in Selector(text=row).css('::text').extract() if a.strip()])

        durations = room_info_table[0][1:]
        altitude_and_prices = room_info_table[1:]

        room_variants = []
        for altitude_and_price in altitude_and_prices:
            for duration, price in zip(durations, altitude_and_price[1:]):
                room_info = {
                    'min_duration': int(duration.split(' ')[0]) * 7,
                    'room_name': f'{apartment_name} {altitude_and_price[0]}',
                    'room_price': price.split(' ')[0]
                }
                room_variants.append(room_info)
        return room_variants

    def extract_without_table_room_variants(self, response):
        apartment_name = self.extract_apartment_name(response)

        css = '.room-type-pricebreakdown ::text'
        duration_and_prices = response.css(css).extract()

        rooms_variants = []
        for duration_and_price in duration_and_prices:
            duration, duration_and_price = self.duration_price_regex.findall(duration_and_price)[0]
            room_info = {
                "min_duration": self.duration_map.get(duration),
                "room_name": apartment_name,
                "room_price": duration_and_price,
            }
            rooms_variants.append(room_info)

        return rooms_variants

    def has_no_table(self, response):
        return not response.css('thead th').extract()

    def detect_availability(self, response):
        button_css = '.button-max::text, .et_pb_button ::text'
        if response.css(button_css).extract_first() == 'Book Now':
            return 'Available'
        return 'Fully Booked'

    def extract_contact_info(self, response):
        reg = re.compile('.*#uber-google-map.*', re.S)
        script = response.css('script::text').re_first(reg, default='')

        raw_contact_info = self.contact_info_regex.findall(script)
        for contact_info in raw_contact_info:
            if contact_info[0] in self.extract_property_name(response):
                return list(contact_info[1:])
        return []

    def extract_room_photos(self, response):
        peel_latrobe_css = '.et_pb_image img::attr(src)'
        photos = response.css(peel_latrobe_css).extract()

        css = '.flexslider-roomtype li::attr(style)'
        return sum([self.images_regex.findall(a) for a in response.css(css).extract()], photos)

    def extract_property_images(self, response):
        new_format_css = '.et_pb_lightbox_image::attr(href)'
        property_images = response.css(new_format_css).extract()

        legacy_format_css = '.slides li::attr(style)'
        return sum([self.images_regex.findall(a) for a in response.css(legacy_format_css).extract()], property_images)

    def extract_floor_plan(self, response):
        id_css = '.wp-image-423::attr(data-izimodal-open)'
        div_id = response.css(id_css).extract_first()
        
        css = f'.floorplan-thumbnail a::attr(data-featherlight), {div_id} img::attr(src)'
        return response.css(css).extract()

    def extract_room_amenities(self, response):
        css = '.et_pb_column li ::text, .home-icon-grid-inner-container p::text'
        return response.css(css).extract()

    def extract_property_amenities(self, response):
        new_format_css = '#facilities .et_pb_blurb_description ::text'
        amenities = set([d.strip() for d in response.css(new_format_css).extract()])

        legacy_format_css = '.home-icon-grid-contents p::text'
        return response.css(legacy_format_css).extract() + list(amenities)

    def extract_property_name(self, response):
        for name_str, name in self.name_map:
            if name_str in response.url:
                return name

    def extract_property_description(self, response):
        new_format_css = '.et_pb_fullwidth_header_subhead::text, #hero p::text'
        description = list(set(response.css(new_format_css).extract()))

        legacy_format_css = '[itemprop="articleBody"] ::text'
        return response.css(legacy_format_css).extract() + description

    def extract_apartment_name(self, response):
        css = '.page-title ::text, h4::text'
        return response.css(css).extract_first()

    def extract_deals(self, response):
        css = '.wrap.cf.two-column-padding p:first-of-type::text'
        return response.css(css).extract()
