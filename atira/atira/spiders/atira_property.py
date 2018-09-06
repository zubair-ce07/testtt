import re

from scrapy import Spider

from ..items import PropertyItem


class PropertyParser(Spider):

    name = "atira-parse"

    min_durations = {'1': 119, '2': 308}

    def parse(self, response):
        atira_property = response.meta.get('a_property', PropertyItem())
        atira_property['property_url'] = response.url
        atira_property['room_photos'] = self.room_photos(response)
        atira_property['room_availability'] = self.room_availability(response)
        atira_property['room_amenities'] = self.room_amenities(response)
        atira_property['floor_plans'] = self.floor_plans(response)
        atira_property['room_type'] = self.room_type(response)

        if response.css('.tablepress'):
            yield from self.extract_room_variants(response, atira_property)
        else:
            yield from self.extract_room_without_table(response, atira_property)

    def room_photos(self, response):
        css = '#carousel .slides img::attr(src)'
        return response.css(css).extract()

    def room_availability(self, response):
        if response.css('.button-max'):
            return "Available"
        return "Fully Booked"

    def room_amenities(self, response):
        return response.css('.d-1of4 p::text').extract()

    def floor_plans(self, response):
        css = '.button-blue-ghost::attr(data-featherlight)'
        return response.css(css).extract()

    def extract_room_variants(self, response, atira_property):
        table = response.css('table')
        room_name = self.room_name(response)
        for row in table.css('tbody tr'):

            if row.css('.column-1:contains(Semester)'):
                prices = row.css('td')[1:]
                duration = row.css('.column-1::text').extract_first().split()[0]
            else:
                name = row.css('.column-1::text').extract_first()
                room_name = name if name else room_name
                prices = row.css('td')[2:]
                duration = row.css('.column-2::text').extract_first().split()[0]

            room = {'prices': prices, 'name': room_name, 'duration': duration}
            yield from self.extract_prices(response, room, atira_property)

    def extract_prices(self, response, room, atira_property,):
        table_header = response.css('thead tr')
        room_name = room['name']
        duration = room['duration']
        prices = room['prices']
        atira_property['min_duration'] = self.min_durations[duration]

        for price in prices:
            atira_property = atira_property.copy()
            class_name = price.css('::attr(class)').extract_first()
            room_view = table_header.css(f'.{class_name} ::text').extract()
            atira_property['room_name'] = f'{room_name} {"".join(room_view)}'
            price = price.css('::text').extract_first().split()[0]
            if 'N/A' not in price:
                atira_property['room_price'] = f'{price} pw'
                yield atira_property

    def extract_room_without_table(self, response, atira_property):
        atira_property['room_name'] = self.room_name(response)
        pattern = re.compile(f'(\d+) Semester[s]? From (.+?) p/week')
        css = '.room-type-pricebreakdown ::text'
        room_variants = response.css(css).extract()
        for room in room_variants:
            atira_property = atira_property.copy()
            duration, price = pattern.findall(room)[0]
            atira_property['min_duration'] = self.min_durations[duration]
            atira_property['room_price'] = f'{price} pw'
            yield atira_property

    def room_name(self, response):
        css = '.page-title::text'
        name = response.css(css).extract_first()
        return re.split(" –|-", name)[0]

    def room_type(self, response):
        seats = self.seats_number(response)
        if "Studio" in self.room_name(response):
            return "entire-room"
        elif int(seats) > 1:
            return "shared-room"
        return "private-room"

    def seats_number(self, response):
        room_utilities = response.css('.room-type-price ul li')
        for utility in room_utilities:
            if utility.css('.fa-bed'):
                seats = utility.css(' ::text').extract()
                return ''.join(seats).strip()
