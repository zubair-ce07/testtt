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


class EvophillySpider(BaseParseSpider, Mixin):
    name = Mixin.name + '-parse'

    def parse(self, response):
        loader = RoomLoader(item=Room(), response=response, date_format='%B %d, %Y')
        loader.add_value('property_name', 'evo Philly')
        loader.add_value('landlord_slug', self.landlord_slug)
        loader.add_value('property_url', response.meta['property_url'])
        loader.add_value('property_contact_info', response.meta['property_contact_info'])
        loader.add_value('property_amenities', response.meta['property_amenities'])
        loader.add_value('property_images', response.meta['property_images'])
        loader.add_value('property_description', response.meta['property_description'])
        common_room = loader.load_item()

        for rooms_sel in response.css('.js-select-floorplan'):
            url = clean(response.css('#application_location ::attr(action)'))[0]
            form_data = {
                'current_navigation_url': '',
                'is_from_navigation_button': '0',
                'application[space_configuration_id]': clean(response.css('#space_configuration_id ::attr(value)'))[0],
                'application[desired_rent_min]': clean(rooms_sel.css('::attr(fp_min_rent)'))[0],
                'application[desired_rent_max]': clean(rooms_sel.css('::attr(fp_max_rent)'))[0],
                'application[lease_start_window_id]': response.meta['planid'],
                'application[property_floorplan_id]': clean(response.css('::attr(value)'))
            }
            yield FormRequest(url=url, formdata=form_data, callback=self.request_room, meta={'room': common_room})

    def request_room(self, response):
        return Request(url=self.room_data_url, callback=self.parse_room, meta={'room': response.meta['room']})

    def parse_room(self, response):
        raw_room = response.meta['room']
        loader = RoomLoader(item=raw_room, response=response)
        loader.add_css('room_name', '.selected-unit-name ::text')
        loader.add_value('room_amenities', self.amenities(response))
        loader.add_value('room_availability', 'available')
        loader.add_value('move_in_date', self.moveindate(response))
        loader.add_value('move_out_date', self.moveindate(response))
        loader.add_value('room_price', self.room_price(response))
        loader.add_value('deposit_amount', self.room_deposit(response))
        return loader.load_item()

    def room_deposit(self, response):
        deposit_sel = response.css('.shopping-cart')
        return clean(deposit_sel.css('.pay-total.js-pay-total ::text'))

    def room_price(self, response):
        price_sel = response.css('#rental-options')
        return clean(price_sel.css('.item-price span::text'))

    def amenities(self, response):
        amenities = []
        for aminiti in response.css('.unit-details-item'):
            title = (clean(aminiti.css('.title ::text')) or [''])[0]
            value = (clean(aminiti.css('.value ::text')) or [''])[0]
            amenities.append(f'{title}:{value}')
        return amenities

    def date_format(self, in_out_date):
        indate = datetime.strptime(in_out_date, "%b %d, %Y").date()
        return indate.strftime('%B %d, %Y')

    def moveindate(self, response):
        move_in_date = clean(response.css('#cart-movein-date ::text'))[0]
        return self.date_format(move_in_date)


class EvophillyCrawler(BaseCrawlSpider, Mixin):
    name = Mixin.name + '-crawl'
    parse_spider = EvophillySpider()
    property_amenities = []
    property_images = []
    decription = ''

    def start_requests(self):
        yield Request(url=self.url, callback=self.parse_description)
        yield Request(url=self.url+'amenities', callback=self.parse_amenities)
        yield Request(url=self.url+'apply', callback=self.parse_login_page)

    def parse_description(self, response):
        self.decription = clean(response.css('.pane-node-body .field--body p::text'))[0]

    def parse_amenities(self, response):
        self.property_amenities = clean(response.css('.pane-amenities-list p::text'))
        self.property_images = clean(response.css('.photoswipe-gallery img::attr(src)'))

    def parse_login_page(self, response):
        url = clean(response.css('#returning_applicants_login ::attr(action)'))[0]
        form_data = {
            'applicant[username]': 'qwe@gmail.com',
            'applicant[password]': 'asd123'
        }
        yield FormRequest(url, formdata=form_data, callback=self.parse_login)

    def parse_login(self, response):
        url = clean(response.css('.btn.js-app-nav ::attr(href)'))[0]
        yield Request(url, self.request_plans)

    def request_plans(self, response):
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
            'planid': plan_id,
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
