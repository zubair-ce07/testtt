import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy import Request
from datetime import datetime, timedelta, date


from ..items import Room, RoomLoader
from .base import BaseCrawlSpider, BaseParseSpider


class Mixin:
    name = landlord_slug = 'staytoo'
    allowed_domains = ['staytoo.de', 'immoblueplus.aareon.com']
    start_urls = ['https://www.staytoo.de/en/']
    landlord_name = 'Staytoo'
    deposit_amount = '400'
    deposit_name = 'deposit'
    deposit_type = 'fixed'
    room_availability = 'Fully Booked'
    e_mail = 'booking@staytoo.de'


class StaytooParseSpider(BaseParseSpider, Mixin):
    name = Mixin.name + '-parse'

    description_css = 'section:not(.color_custom):not(.color_footer-bottom) p::text'
    description_re = r'[^\s|][\w .,?]*'

    max_prices = {
        'SingleStudio': 700, 'DoubleStudio': 900, 'BusinessStudio': 1200
    }

    def parse(self, response):
        loader = RoomLoader(item=Room(), response=response)
        loader.add_value('room_amenities', self.room_amenities(response))
        meta = {'item': loader.load_item()}
        cities_css = '#menu-item-20479 .level_2 a::attr(href)'

        for cities in response.css(cities_css).extract():
            yield Request(url=cities, callback=self.parse_city, meta=meta)

    def parse_city(self, response):
        loader = RoomLoader(item=response.meta['item'], response=response)
        loader.add_xpath('property_amenities', self.property_amenities(response))
        loader.add_value('deposit_amount', self.deposit_amount)
        loader.add_value('deposit_name', self.deposit_name)
        loader.add_value('deposit_type', self.deposit_type)
        loader.add_value('room_availability', self.room_availability)
        move_in_date = self.move_in_date()
        loader.add_value('move_in_date', move_in_date)
        loader.add_value('move_out_date', self.move_out_date(move_in_date))
        loader.add_value('property_slug', self.property_slug(response.url))
        loader.add_value('landlord_slug', self.landlord_slug)
        loader.add_value('property_name', self.property_name(response))
        loader.add_value('property_url', response.url)
        loader.add_css('property_description', self.description_css, re=self.description_re)
        loader.add_value('property_contact_info', self.property_contact_info(response))
        floor_plan_css = 'img[src$="plan.png"]::attr(src)'
        loader.add_css('floor_plans', floor_plan_css)
        room_photos_css = 'img[src*="Apartment"]::attr(src)'
        loader.add_css('room_photos', room_photos_css)
        base_item = loader.load_item()

        yield from self.city_request(response, base_item.copy())

    def city_request(self, response, base_item):
        city_re = r'en/(\w+)-'
        city = re.search(city_re, response.url).group(1)

        meta = {'item': base_item, 'city': city}
        url_css = 'a.w-btn::attr(href)'
        url = response.css(url_css).extract_first()

        yield Request(url=url, callback=self.city_request_chain, meta=meta.copy())

    def city_request_chain(self, response):
        url_re = r'var url = \'([\w.:/=?]+)\';'
        url_css = 'section#aareonSection script'
        u = response.css(url_css).re_first(url_re)

        yield Request(url=u, callback=self.parse_rooms, meta=response.meta.copy())

    def parse_rooms(self, response):
        data_place = self.data_place(response)
        room_xpath = '//select[@name="apartmentType"]'
        room_css = f'option[data-places*="{data_place}"]'

        for room_sel in response.xpath(room_xpath).css(room_css):
            room_name_css = '::attr(data-lang-id)'
            room_name_re = r'Type(\w+)'
            room_name = room_sel.css(room_name_css).re_first(room_name_re)
            room_min_price_css = '::attr(data-minprice)'
            room_min_price = room_sel.css(room_min_price_css).extract_first()

            yield from self.parse_room(room_name, room_min_price, response, data_place)

    def parse_room(self, room_name, min_price, response, data_place):
        room_prices = self.room_prices(room_name, min_price, response, data_place)

        for price in room_prices:
            loader = RoomLoader(item=response.meta.get('item'), response=response)
            loader.add_value('room_name', room_name)
            loader.add_value('room_price', str(price))

            yield loader.load_item()

    def room_prices(self, room_name, min_price, response, data_place):
        room_xpath = '//select[@name="maxPrice"]'
        room_css = f'option[data-places*="{data_place}"]::attr(value)'
        room_prices = response.xpath(room_xpath).css(room_css).extract()

        min_price = int(min_price) if min_price else 500
        max_price = self.max_prices[room_name]

        def filter_prices(x):
            return min_price <= int(x) <= max_price

        return list(filter(filter_prices, room_prices))

    def move_in_date(self):
        dd = 1
        mm = 11
        yy = int(datetime.now().year)

        return date(yy, mm, dd).strftime('%d/%m/%y')

    def move_out_date(self, move_in_date):
        move_in_date = datetime.strptime(move_in_date, '%d/%m/%y')
        move_out_date = move_in_date + timedelta(days=364)

        return move_out_date.strftime('%d/%m/%y')

    def property_name(self, response):
        css = 'h2 ::text'
        name = response.css(css).extract_first().split(' ')[0]
        name = f'{name} Student Apartments - Staytoo'

        return name

    def property_slug(self, url):
        city_name_re = r'en/(\w+)-'
        city_name = re.search(city_name_re, url).group(1)

        return f'{self.landlord_name}-{city_name}'

    def data_place(self, response):
        room_name = response.meta.get('city')
        data_place_css = f'select[name="location"] option:contains({room_name[-3:]})::attr(value)'

        return int(response.css(data_place_css).extract_first())

    def property_amenities(self, response):
        property_amenities_css = 'h5::text'
        property_amenities_re = r'.+(?<!Extra)$'

        return response.css(property_amenities_css).re(property_amenities_re)

    def property_contact_info(self, response):
        telephone_css = 'a[href^="tel"]::attr(href)'
        telephone_re = r'tel:([+\d ]+)'
        telephone = response.css(telephone_css).re_first(telephone_re)

        return [telephone, self.e_mail]

    def room_amenities(self, response):
        amenities_css = 'div.ult_exp_content'
        amenities_xpath = './/h5/text()'
        amenities_re = r'.+(?<!Extra)$'
        amenities_section = response.css(amenities_css)[0]

        return amenities_section.xpath(amenities_xpath).re(amenities_re)


class StaytooSpider(BaseCrawlSpider, Mixin):
    name = Mixin.name + '-crawl'
    custom_settings = {
        'COOKIES_ENABLED': False
    }

    parse_spider = StaytooParseSpider()

    english_url = 'li>a[href$="/en/apartments/"]'
    rules = [
        Rule(LinkExtractor(restrict_css=english_url), 'parse_item'),
    ]

