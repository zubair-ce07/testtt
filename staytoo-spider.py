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
    start_urls = ['https://www.staytoo.de/']
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
        property_amenities_xpath = '(//section[12]|//section[13])//p/text()'
        loader.add_xpath('property_amenities', property_amenities_xpath)
        meta = {'item': loader.load_item()}
        cities_css = '#menu-item-20479 .level_2 a::attr(href)'
        for cities in response.css(cities_css).extract():
            yield Request(url=cities, callback=self.parse_city, meta=meta.copy())

    def parse_city(self, response):
        loader = RoomLoader(item=response.meta['item'], response=response)
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
        telephone_css = 'a[href^="tel"]::attr(href)'
        telephone_re = r'tel:([+\d ]+)'
        loader.add_css('property_contact_info', telephone_css, re=telephone_re)
        loader.add_value('property_contact_info', self.e_mail)
        floor_plan_css = 'img[src$="plan.png"]::attr(src)'
        loader.add_css('floor_plans', floor_plan_css)
        room_photos_css = 'img[src*="Apartment"]::attr(src)'
        loader.add_css('room_photos', room_photos_css)

        yield from self.city_request(response, loader.load_item())

    def city_request(self, response, item):
        city_re = r'en/(\w+)-'
        meta = {'item': item, 'city': re.search(city_re, response.url).group(1)}
        url_css = 'a.w-btn::attr(href)'
        url = response.css(url_css).extract_first()

        yield Request(url=url, callback=self.city_request_chain, meta=meta.copy())

    def city_request_chain(self, response):
        url_re = r'var url = \'([\w.:/=?]+)\';'
        url_css = 'section#aareonSection script'
        u = response.css(url_css).re_first(url_re)

        yield Request(url=u, callback=self.parse_rooms, meta=response.meta.copy())

    def parse_rooms(self, response):
        data_place = self.data_place(response.meta['city'], response)
        response.meta['data_place'] = data_place
        room_xpath = '//select[@name="apartmentType"]'
        room_css = f'option[data-places*="{data_place}"]'

        for room_sel in response.xpath(room_xpath).css(room_css):
            room_name_css = '::attr(data-lang-id)'
            room_name_re = r'Type(\w+)'
            room_name = room_sel.css(room_name_css).re_first(room_name_re)
            room_min_price_css = '::attr(data-minprice)'
            room_min_price = room_sel.css(room_min_price_css).extract_first()

            yield from self.parse_room(room_name, room_min_price, response)

    def parse_room(self, room_name, min_price, response):
        room_prices = self.room_prices(room_name, min_price, response)

        for price in room_prices:
            loader = RoomLoader(item=response.meta['item'], response=response)
            loader.add_value('room_name', room_name)
            loader.add_value('room_price', str(price))

            yield loader.load_item()

    def room_prices(self, room_name, min_price, response):
        data_place = response.meta['data_place']
        room_xpath = '//select[@name="maxPrice"]'
        room_css = f'option[data-places*="{data_place}"]::attr(value)'
        room_prices = response.xpath(room_xpath).css(room_css).extract()

        min_price = int(min_price) if min_price else 500
        max_price = self.max_prices[room_name]

        def filter_prices(x):
            return min_price <= int(x) <= max_price

        return list(filter(filter_prices, room_prices))

    def move_in_date(self):
        mm = (int(datetime.now().month) % 12) + 1
        yy = int(datetime.now().year)

        return date(yy, mm, 1).strftime('%d/%m/%y')

    def move_out_date(self, move_in_date):
        move_in_date = datetime.strptime(move_in_date, '%d/%m/%y')
        move_out_date = move_in_date + timedelta(days=364)

        return move_out_date.strftime('%m/%d/%y')

    def property_name(self, response):
        css = 'h2 ::text'
        name = response.css(css).extract_first().split(' ')[0]
        name = f'{name} Student Apartments - Staytoo'

        return name

    def property_slug(self, url):
        city_name_re = r'en/(\w+)-'
        city_name = re.search(city_name_re, url).group(1)

        return f'{self.landlord_name}-{city_name}'

    def data_place(self, room_name, response):
        data_place_css = f'select[name="location"] option:contains({room_name[-3:]})::attr(value)'
        return int(response.css(data_place_css).extract_first())


class StaytooSpider(BaseCrawlSpider, Mixin):
    name = Mixin.name + '-crawl'
    custom_settings = {
        'COOKIES_ENABLED': False
    }

    parse_spider = StaytooParseSpider()

    english_url = 'a.w-dropdown-item:first-child'
    rules = [
        Rule(LinkExtractor(restrict_css=english_url), 'parse_item'),
    ]

