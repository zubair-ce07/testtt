
from datetime import datetime

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from student.items import Room, RoomLoader
from .base import BaseCrawlSpider, BaseParseSpider
from ..utils import clean


class Mixin:
    name = 'iqstudent'
    allowed_domains = ['iqstudentaccommodation.com']
    start_urls = ['https://www.iqstudentaccommodation.com/']
    landlord_slug = 'iqstudent-property-group-pty-ltd'
    landlord_name = 'Iqstudent Property Group Pty Ltd'


class IQStudentAccommodationSpider(BaseParseSpider, Mixin):
    name = Mixin.name + '-parse'

    def parse(self, response):
        loader = RoomLoader(item=Room(), response=response, date_format='%B %d, %Y')
        loader.add_value('property_name', response.meta['property_name'])
        loader.add_value('landlord_slug', self.landlord_slug)
        loader.add_value('property_url', response.meta['property_url'])
        loader.add_value('property_description', response.meta['property_description'])
        loader.add_value('property_amenities', response.meta['property_amenities'])
        loader.add_value('property_contact_info', response.meta['property_contact_info'])
        loader.add_css('room_name', '.slidertext span ::text')
        loader.add_css('room_amenities', '.left-intro.room-type .sprite-before.star ::text')
        loader.add_css('room_photos', '.carousel img::attr(src)')
        rooms = iter(response.css('.divTable .divTableBody .divTableRow'))
        next(rooms)
        for row in rooms:
            cells = clean(row.css('.divTableCell ::text'))
            loader.add_value('room_availability', cells[5])
            loader.add_value('move_in_date', self.date_format(cells[1]))
            loader.add_value('move_out_date', self.date_format(cells[2]))
            loader.add_value('deposit_amount', cells[3])
            loader.add_value('room_price', cells[4])
            yield loader.load_item().copy()

    def date_format(self, in_out_date):
        indate = datetime.strptime(in_out_date, "%d/%m/%Y").date()
        return indate.strftime('%B %d, %Y')


class IQStudentAccommodationCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.name + '-crawl'
    parse_spider = IQStudentAccommodationSpider()
    listing_css = '.sub-menu.level-2'

    rules = [
        Rule(LinkExtractor(restrict_css=listing_css, tags='a', attrs='href'), callback='parse_property'),
    ]

    def parse_property(self, response):
        meta = {
            'property_url': response.url,
            'property_name': clean(response.css('.phone-title ::text'))[0],
            'property_description': clean(response.css('#overview ~ p::text')) or [],
            'property_amenities': clean(response.css('.sprite-before.odd.star ::text')),
            'property_contact_info': clean(response.css('.new-contact-details >p ::text'))
        }
        rooms_urls = clean(response.css('.button.cta-small.btnsite ::attr(href)'))
        for url in rooms_urls:
            yield Request(url=response.urljoin(url), callback=self.parse_item, meta=meta)


