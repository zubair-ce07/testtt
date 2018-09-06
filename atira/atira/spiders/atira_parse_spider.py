import copy
import json
import re
from datetime import datetime
from urllib import parse

from scrapy.spiders import Spider

from atira.items import Product


class AtiraParseSpider(Spider):
    name = "atira_parser"
    price_raw_map = {"p/week", "Per Week", "Per week", "per week"}
    price_notation = "pw"

    def parse(self, response):
        item = Product()
        response.meta['item'] = item
        return self.request_deals(response)

    def parse_deals(self, response):
        item = response.meta['item']
        css = '.content-content p::text'
        item['deals'] = [response.css(css).extract_first()]
        response.meta['item'] = item

        return self.property_details(response.meta['main_response'])

    def parse_further_detail(self, response):
        item = response.meta['item']
        item = self.property_main_details(response, item)

        for request in response.meta['room_requests']:
            request.meta['item'] = copy.copy(item)
            yield request

    def parse_room_details(self, response):
        item = response.meta['item']
        item = self.room_main_details(response, item)
        item = self.property_common_details(item)
        room_name = self.room_name(response)
        pricing_info = self.pricing_breakdown(response)
        yield from self.room_variant_details(item, pricing_info, room_name)

    def request_deals(self, response):
        css = 'a:contains("Offer")::attr(href)'
        url = response.css(css).extract_first()

        if not url:
            return self.property_details(response)

        request = response.follow(url, dont_filter=True, callback=self.parse_deals)
        request.meta['main_response'] = response
        request.meta['item'] = response.meta['item']

        return request

    def property_details(self, response):
        item = response.meta['item']
        item['property_description'] = self.property_description(response)
        item['property_name'] = self.property_name(response)
        item['property_contact_info'] = self.property_contact_info(response)
        room_requests = self.room_requests(response)

        if not room_requests:
            return self.room_details(response)

        return self.room_further_details(response, room_requests, item)

    def room_requests(self, response):
        css = '.room-type-container a::attr(href), ' \
                   'h6:contains("VIEW ROOM") ::attr(href)'
        room_urls = response.css(css).extract()

        requests = []
        for url in room_urls:
            requests.append(response.follow(url, callback=self.parse_room_details))

        return requests

    def room_details(self, response):
        parent_item = response.meta['item']
        parent_item = self.property_main_details(response, parent_item)

        for room_sel in response.css('.et_pb_column'):
            main_item = copy.copy(parent_item)
            main_item = self.room_main_details(response, main_item)
            main_item = self.property_common_details(main_item)
            room_name = self.room_name(room_sel)
            pricing_info = self.pricing_breakdown_same_page(room_sel)
            yield from self.room_variant_details(main_item, pricing_info, room_name)

    def room_further_details(self, response, room_requests, item):
        css = '.grid-seemore::attr(href)'
        url = response.css(css).extract_first()

        if not url:
            response.meta['room_requests'] = room_requests
            response.meta['item'] = item
            return self.parse_further_detail(response)

        request = response.follow(url, callback=self.parse_further_detail)
        request.meta['room_requests'] = room_requests
        request.meta['item'] = item

        return request

    def property_main_details(self, response, item):
        item['property_amenities'] = self.property_amenities(response)
        item['property_images'] = self.property_images(response)

        return item

    @staticmethod
    def property_common_details(item):
        item['landlord_slug'] = "atira-student-living"
        item['listing_type'] = "flexible_open_end"
        item['deposit_type'] = "fixed"
        item['deposit_name'] = "deposit"
        item['available_from'] = datetime.today().strftime('%Y-%m-%d')

        return item

    def room_main_details(self, response, item):
        item['property_url'] = response.url
        item['room_photos'] = self.property_images(response)
        item['room_availability'] = self.room_availability(response)
        item['room_amenities'] = self.property_amenities(response)
        item['floor_plans'] = self.floor_plans(response)

        return item

    @staticmethod
    def room_variant_details(main_item, pricing_details, room_name):
        for variant in pricing_details:
            item = copy.copy(main_item)
            item['room_type'] = variant['type']
            item['room_price'] = variant['price']
            item['room_name'] = f"{room_name} {variant['type']}"
            item['min_duration'] = variant['duration']
            item['product_id'] = f"{room_name}_{variant['type']}_{variant['duration']}"

            yield item

    @staticmethod
    def property_name(response):
        css = '.flexslider-caption ::text, link ::attr(title)'
        return response.css(css).extract_first().split('-')[0]

    @staticmethod
    def property_description(response):
        css = '.et_pb_text_inner p::text, .entry-content ::text'
        return response.css(css).extract_first()

    @staticmethod
    def map_info(response):
        css = '.location-map-container ::attr(id)'
        map_id = response.css(css).extract_first()

        pattern = f"#{map_id}'\).UberGoogleMaps\((.*?)\);\s*$"
        info = re.findall(pattern, response.text, re.M)
        if info:
            return info[0]

    def property_contact_info(self, response):
        map_info = self.map_info(response)

        if not map_info:
            css = '#footer-info a ::text'
            return [response.css(css).extract_first()]

        for info in json.loads(map_info)['infoWindows']:
            if info['open'] is not '1':
                continue

            return [info['phone'], info['email']]

    @staticmethod
    def room_amenities(response):
        css = '.et_pb_column li ::text'
        return response.css(css).extract()

    @staticmethod
    def property_amenities(response):
        css = '[data-key="sameHeights"] p::text, '\
                     '#facilities .et_pb_blurb_description ::text'
        amenities = response.css(css).extract()
        return list(set([text.strip() for text in amenities if text.strip()]))

    @staticmethod
    def property_images(response):
        pattern = re.compile(r"url\((.*?)\)")
        galary_css = '.et_pb_lightbox_image ::attr(href)'
        img_css = '.et_pb_image_wrap ::attr(src)'
        images =  response.xpath('//ul[@class="slides"]').re(pattern)\
                  or response.css(galary_css).extract()\
                  or [response.css(img_css).extract_first()]

        return images

    @staticmethod
    def room_availability(response):
        css = '.room-type-price:contains("Book"), ' \
              '.et_pb_button_module_wrapper:contains("Book")'
        if response.css(css):
            return "Availabale"

        return "Not Available"

    @staticmethod
    def floor_plans(response, url=None):
        if not url:
            css = '.floorplan-thumbnail ::attr(data-featherlight)'
            return response.css(css).extract()

        floor_plan = []
        for fp in response.css('img::attr(src)').extract():
            if "floorplan" in fp:
                floor_plan.append(parse.urljoin(url, fp))

        return floor_plan

    @staticmethod
    def room_name(response):
        css = '.page-title ::text,'\
              '.et_pb_column .et_pb_text_inner h4 ::text'
        return response.css(css).extract_first()

    @staticmethod
    def high_view_class_name(response):
        css = 'th:contains("High")::attr(class)'
        return response.css(css).extract_first()
    
    @staticmethod
    def low_view_class_name(response):
        css = 'th:contains("Low")::attr(class)'
        return response.css(css).extract_first()
        
    @staticmethod
    def semester_class_name(response):
        css = 'td:contains("Semester")::attr(class)'
        return response.css(css).extract_first()

    def refine_price(self, price):
        if not price:
            return None

        for notation in self.price_raw_map:
            if notation in price:
                return price.replace(notation, self.price_notation)

        return f"{price} {self.price_notation}"

    def room_price(self, view_class, table_row):
        price_css = f'.{view_class} ::text'
        return self.refine_price(table_row.css(price_css).extract_first())

    @staticmethod
    def pricing_details(title, price, duration, room_type):
        element = {}
        element['title'] = title
        element['price'] = price
        element['type'] = room_type
        element['duration'] = duration

        return element

    def pricing_breakdown(self, response):
        response = response.css('.tablepress')
        
        high_view_class = self.high_view_class_name(response)
        low_view_class = self.low_view_class_name(response)
        sem_class = self.semester_class_name(response)

        price_details = []
        title = None
        for table_row in response.css('tbody tr'):
            duration = "119"
            sem_css = f'.{sem_class}:contains("2 Semester")'

            if table_row.css(sem_css):
                duration = "308"

            column1_info = table_row.css('.column-1 ::text').extract_first()

            if sem_class != "column-1" and column1_info:
                title = column1_info

            avail_css = f'.{low_view_class}:contains("N/A")'
            if not table_row.css(avail_css).extract_first() and low_view_class:
                price = self.room_price(low_view_class, table_row)
                price_details.append(self.pricing_details(title, price,
                                                          duration, "Low View"))

            avail_css = f'.{high_view_class}:contains("N/A")'
            if not table_row.css(avail_css).extract_first() and high_view_class:
                price = self.room_price(high_view_class, table_row)
                price_details.append(self.pricing_details(title, price,
                                                          duration, "High View"))

        return price_details

    def pricing_breakdown_same_page(self, response):
        price_details = []
        for row in response.css('tbody tr+tr'):
            room = row.css('td:nth-child(1) ::text').extract_first()
            name = self.room_name(response)

            price = self.refine_price(row.css('td:nth-child(2) ::text').extract_first())
            if price:
                price_details.append(self.pricing_details(name, price, "357", room))

            price = self.refine_price(row.css('td:nth-child(3) ::text').extract_first())
            if price:
                price_details.append(self.pricing_details(name, price, "336", room))

            price = self.refine_price(row.css('td:nth-child(4) ::text').extract_first())
            if price:
                price_details.append(self.pricing_details(name, price, "168", room))

        return price_details
