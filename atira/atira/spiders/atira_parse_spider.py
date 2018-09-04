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

    def parse_item(self, response):
        item = response.meta['item']
        item['property_description'] = self.property_description(response)
        item['property_name'] = self.property_name(response)
        item['landlord_slug'] = "atira-student-living"
        item['property_contact_info'] = self.property_contact_info(response)
        response.meta[item] = item
        room_requests = self.room_requests(response)

        if not room_requests:
            return self.parse_room_same_page(response)

        return self.room_further_details(response, room_requests, item)

    def parse_further_detail(self, response):
        item = response.meta['item']
        item['property_amenities'] = self.property_amenities(response)
        item['property_images'] = self.property_images(response)

        for request in response.meta['room_requests']:
            request.meta['item'] = copy.deepcopy(item)
            yield request

    def parse_room_same_page(self, response):
        parent_item = response.meta['item']
        parent_item['property_amenities'] = self.property_amenities(response)
        parent_item['property_images'] = self.property_images(response)
        parent_item['property_url'] = response.url

        for res in response.css('.et_pb_column'):
            main_item = copy.deepcopy(parent_item)
            main_item['room_photos'] = self.property_images(res)
            main_item['room_availability'] = self.room_availability(res)
            main_item['room_amenities'] = self.room_amenities(res)
            main_item['floor_plans'] = self.floor_plans(res, response.url)
            main_item['room_name'] = self.room_name(res)
            main_item['listing_type'] = "flexible_open_end"
            main_item['deposit_type'] = "fixed"
            main_item['deposit_name'] = "deposit"
            main_item['available_from'] = datetime.today().strftime('%Y-%m-%d')

            for varient in self.pricing_breakdown_same_page(res):
                item = copy.deepcopy(main_item)
                item['room_type'] = varient[0]
                item['room_price'] = varient[1]
                item['room_name'] = f"{main_item['room_name']} {varient[2]}"
                item['min_duration'] = varient[3]
                item['product_id'] = f"{varient[0]}_{varient[1]}_{varient[3]}"

                yield item


    def parse_room_details(self, response):
        item = response.meta['item']
        item['property_url'] = response.url
        item['room_photos'] = self.property_images(response)
        item['room_availability'] = self.room_availability(response)
        item['room_amenities'] = self.property_amenities(response)
        item['floor_plans'] = self.floor_plans(response)
        item['room_name'] = self.room_name(response)

        item['listing_type'] = "flexible_open_end"
        item['deposit_type'] = "fixed"
        item['deposit_name'] = "deposit"
        item['available_from'] = datetime.today().strftime('%Y-%m-%d')

        prices_info = self.pricing_breakdown(response)
        return self.parse_price_variant(prices_info, item, response)

    def parse_price_variant(self, prices_info, item_parent, response):
        items = []
        for varient in prices_info:
            item = copy.deepcopy(item_parent)
            room_type = varient[0] or "private-room"
            item['room_type'] = room_type
            item['room_price'] = varient[1]
            item['room_name'] = f"{self.room_name(response)} {varient[2]}"
            item['min_duration'] = varient[3]
            item['product_id'] = f"{room_type}_{varient[1]}_{varient[3]}"
            items.append(item)

        return items

    def parse_deals(self, response):
        item = response.meta['item']
        css = '.content-content p::text'
        item['deals'] = [response.css(css).extract_first()]
        response.meta['item'] = item
        return self.parse_item(response.meta['main_response'])

    def request_deals(self, response):
        css = 'a:contains("Offer")::attr(href)'
        url = response.css(css).extract_first()

        if not url:
            return self.parse_item(response)

        request = response.follow(url, dont_filter=True, callback=self.parse_deals)
        request.meta['main_response'] = response
        request.meta['item'] = response.meta['item']

        return request

    def room_requests(self, response):
        room_css = '.room-type-container a::attr(href)'
        view_room_css = 'h6:contains("VIEW ROOM") ::attr(href)'
        room_urls = response.css(room_css).extract() \
                    or response.css(view_room_css).extract()

        requests = []
        for url in room_urls:
            requests.append(response.follow(url, callback=self.parse_room_details))

        return requests

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

    def property_name(self, response):
        css = '.flexslider-caption ::text'
        css2 = 'link ::attr(title)'
        return response.css(css).extract_first() \
               or response.css(css2).extract_first().split('-')[0]

    def property_description(self, response):
        des_css_1 = '.et_pb_text_inner p::text'
        des_css_2 = '.entry-content ::text'
        return response.css(des_css_1).extract_first() \
               or response.css(des_css_2).extract_first()


    def map_info(self, response):
        css = '.location-map-container ::attr(id)'
        map_id = response.css(css).extract_first()
        pattern = f"#{map_id}'\).UberGoogleMaps\((.*?)\);\s*$"
        info = re.findall(pattern, response.text, re.M)
        if info:
            return info[0]

        return []

    def property_contact_info(self, response):
        map_info = self.map_info(response)

        if not map_info:
            css = '#footer-info a ::text'
            return [response.css(css).extract_first()]

        for info in json.loads(map_info)['infoWindows']:
            if info['open'] is not '1':
                continue

            return [info['phone'], info['email']]

        return []

    def room_amenities(self, response):
        same_pg_css = '.et_pb_column li ::text'
        return response.css(same_pg_css).extract()

    def property_amenities(self, response):
        amen_css_1 = '[data-key="sameHeights"] p::text'
        amen_css_2 = '#facilities .et_pb_blurb_description ::text'
        amenities =  response.css(amen_css_1).extract() \
                     or response.css(amen_css_2).extract()
        return list(set([text.strip() for text in amenities if text.strip()]))

    def property_images(self, response):
        pattern = re.compile(r"url\((.*?)\)")
        gal_css = '.et_pb_lightbox_image ::attr(href)'
        img_css = '.et_pb_image_wrap ::attr(src)'
        images =  response.xpath('//ul[@class="slides"]').re(pattern)\
                  or response.css(gal_css).extract() \
                  or [response.css(img_css).extract_first()]

        return images

    def room_availability(self, response):
        other_pg_css = '.room-type-price:contains("Book")'
        same_pg_css = '.et_pb_button_module_wrapper:contains("Book")'
        if response.css(other_pg_css).extract() \
                or response.css(same_pg_css).extract():
            return "Availabale"

        return "Not Available"

    def floor_plans(self, response, url=None):
        css = '.floorplan-thumbnail ::attr(data-featherlight)'
        imgs_css = 'img::attr(src)'

        if not url:
            return response.css(css).extract()

        floor_plan = []
        for fp in response.css(imgs_css).extract():
            if "floorplan" in fp:
                floor_plan.append(parse.urljoin(url, fp))

        return floor_plan


    def room_name(self, response):
        css = '.page-title ::text'
        same_pg_css = '.et_pb_column .et_pb_text_inner h4 ::text'
        name =  response.css(css).extract_first() \
               or response.css(same_pg_css).extract_first()

        return name
    
    def high_view_class_name(self, response):
        high_css = 'th:contains("High")::attr(class)'
        return response.css(high_css).extract_first()
    
    def low_view_class_name(self, response):
        low_css = 'th:contains("Low")::attr(class)'
        return response.css(low_css).extract_first()
        
    def semester_class_name(self, response):
        sem_css = 'td:contains("Semester")::attr(class)'
        return response.css(sem_css).extract_first()

    def refine_price(self, price):
        if not price:
            return None

        for notation in self.price_raw_map:
            if notation in price:
                return price.replace(notation, self.price_notation)

        return f"{price} {self.price_notation}"
    
    def pricing_breakdown(self, response):
        response = response.css('.tablepress')
        
        high_view_class = self.high_view_class_name(response)
        low_view_class = self.low_view_class_name(response)
        sem_class = self.semester_class_name(response)

        body_css = 'tbody tr'
        data = []
        title = None
        for tr in response.css(body_css):
            element = []
            duration = "119"

            p_low_css = f'.{low_view_class}:contains("N/A")'
            if not tr.css(p_low_css).extract_first() and low_view_class:
                if sem_class != "column-1" \
                        and tr.css('.column-1 ::text').extract_first():
                    title = tr.css('.column-1 ::text').extract_first()

                sem_css = f'.{sem_class}:contains("2 Semester")'
                if tr.css(sem_css).extract_first():
                    duration = "308"

                element.append(title)
                price_css = f'.{low_view_class} ::text'
                price = self.refine_price(tr.css(price_css).extract_first())
                element.append(price)
                element.append("Low View")
                element.append(duration)
                data.append(element)

            p_high_css = f'.{high_view_class}:contains("N/A")'
            if not tr.css(p_high_css).extract_first() and high_view_class:
                element = []
                element.append(title)
                price_css = f'.{high_view_class} ::text'
                price = self.refine_price(tr.css(price_css).extract_first())
                element.append(price)
                element.append("High View")
                element.append(duration)
                data.append(element)

        return data

    def pricing_breakdown_same_page(self, response):
        data = []
        for row in response.css('tbody tr+tr'):
            room = row.css('td:nth-child(1) ::text').extract_first()
            if not room:
                continue

            element = []
            element.append(self.room_name(response))
            price = self.refine_price(row.css('td:nth-child(2) ::text').extract_first())
            element.append(price)
            element.append(room)
            element.append("357")
            if price:
                data.append(element)

            element = []
            element.append(self.room_name(response))
            price = self.refine_price(row.css('td:nth-child(2) ::text').extract_first())
            element.append(price)
            element.append(room)
            element.append("336")
            if price:
                data.append(element)

            element = []
            element.append(self.room_name(response))
            price = self.refine_price(row.css('td:nth-child(2) ::text').extract_first())
            element.append(price)
            element.append(room)
            element.append("168")
            if price:
                data.append(element)

        return data

