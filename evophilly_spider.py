import re
from datetime import datetime

from scrapy import Request, FormRequest
from slugify import slugify

from student.items import Room, RoomLoader
from .base import BaseCrawlSpider, BaseParseSpider
from ..utils import clean


class Mixin:
    name = "evophilly"
    allowed_domain = "evophilly.com"
    url = 'http://evophilly.com/'
    room_data_url = 'https://evoatciracentresouth.prospectportal.com/Apartments/module/application_options/'
    landlord_slug = 'evophilly-property-group-pty-ltd'
    landlord_name = slugify('evo Philly Property Group Pty Ltd')
    login_user = 'dak@gmail.com'
    login_password = 'asd123'


class EvophillySpider(BaseParseSpider, Mixin):
    name = Mixin.name + '-parse'

    def parse(self, response):
        plan_dates = self.movein_moveout_dates(response.meta['plan_date'])
        loader = RoomLoader(item=Room(), response=response, date_format='%B %d, %Y')
        loader.add_value('property_name', 'evo Philly')
        loader.add_value('landlord_slug', self.landlord_slug)
        loader.add_value('property_url', response.meta['property_url'])
        loader.add_value('property_contact_info', response.meta['property_contact_info'])
        loader.add_value('property_amenities', response.meta['property_amenities'])
        loader.add_value('property_images', response.meta['property_images'])
        loader.add_value('property_description', response.meta['property_description'])
        loader.add_value('move_in_date', plan_dates[0])
        loader.add_value('move_out_date', plan_dates[1])
        common_room = loader.load_item()

        for room_sel in response.css('.list-item'):
            loader_r = RoomLoader(item=common_room.copy(), selector=room_sel, response=room_sel)
            self.parse_rooms(loader_r)
            yield loader_r.load_item()

    def parse_rooms(self, loader):
        loader.add_css('room_name', '.title-block .title span::text')
        loader.add_css('room_amenities', '.title-block .sub-title ::text')
        loader.add_css('room_photos', '.layout img::attr(src)')
        loader.add_value('room_availability', 'available')
        loader.add_css('room_price', '.room-type-table .room-row .monthly-col::text')

    def movein_moveout_dates(self, in_out_date):
        plan_dates = []
        in_out_dates = in_out_date.split('-')
        for plan_date in in_out_dates:
            plan_dates.append(self.date_format(plan_date))
        return plan_dates

    def date_format(self, plan_date):
        start_end_date = re.search("([0-9]{2}/[0-9]{2}/[0-9]{4})", plan_date)[0]
        indate = datetime.strptime(start_end_date, "%m/%d/%Y").date()
        return indate.strftime('%B %d, %Y')


class EvophillyCrawler(BaseCrawlSpider, Mixin):
    name = Mixin.name + '-crawl'
    parse_spider = EvophillySpider()
    property_amenities = []
    property_images = []
    decription = ''

    def start_requests(self):
        yield Request(url=self.url, callback=self.parse_description)
        yield Request(url=self.url + 'amenities', callback=self.parse_amenities)
        yield Request(url=self.url + 'apply', callback=self.login_page_request)

    def parse_description(self, response):
        self.decription = clean(response.css('.pane-node-body .field--body p::text'))[0]

    def parse_amenities(self, response):
        self.property_amenities = clean(response.css('.pane-amenities-list p::text'))
        self.property_images = clean(response.css('.photoswipe-gallery img::attr(src)'))

    def login_page_request(self, response):
        url = clean(response.css('#returning_applicants_login ::attr(action)'))[0]
        form_data = {
            'applicant[username]': self.login_user,
            'applicant[password]': self.login_password
        }
        yield FormRequest(url, formdata=form_data, callback=self.parse_login)

    def parse_login(self, response):
        url = clean(response.css('.btn.js-app-nav ::attr(href)'))[0]
        yield Request(url, self.plans_request)

    def plans_request(self, response):
        url = clean(response.css('#lease_start_window_id ::attr(data-url)'))[0]
        plan_sel = response.css('.vertform-item.radio')
        plan_id = clean(plan_sel[1].css('.js-select-lease-start-window ::attr(value)'))[0]
        plan_date = clean(plan_sel[1].css('label ::text'))[0]
        meta = {
            'property_amenities': self.property_amenities,
            'property_images': self.property_images,
            'property_url': self.url,
            'property_contact_info': self.contact_info(response.css('.vcard')),
            'property_description': self.decription,
            'plan_date': plan_date,
        }
        yield Request(url=url + plan_id, callback=self.parse_item, meta=meta)

    def contact_info(self, contact_sel):
        contact_info = []
        contact_info.append(clean(contact_sel.css('.street-address ::text'))[0])
        contact_info.append(clean(contact_sel.css('.locality ::text'))[0])
        contact_info.append(clean(contact_sel.css('.region ::text'))[0])
        contact_info.append(clean(contact_sel.css('.postal-code ::text'))[0])
        contact_info.append(clean(contact_sel.css('.google-forwarding-number ::attr(href)'))[0])
        contact_info.append(clean(contact_sel.css('.fax ::attr(href)'))[0])
        return contact_info
