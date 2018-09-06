import re

from scrapy.spidermiddlewares.httperror import HttpError
from datetime import datetime
from scrapy import Request, FormRequest
from scrapy import signals

from student.utils import clean
from ..items import Room, RoomLoader
from .base import BaseCrawlSpider, BaseParseSpider


class BaseMixinPP:
    login_url_t = '{}/Apartments/module/application_authentication'
    amenities_url_t = '{}/amenities'
    floor_amenities_url_t = '{}/floorplans'
    contact_url_t = '{}/contact'
    unit_info_url_t = '{}/Apartments/module/application_unit_info/'
    login_email = 'james.henry1786@gmail.com'
    login_password = '0b006edd3ee1862c8efcb7bf8052a278'
    first_name = "james"
    last_name = "henry"
    phone_num = "333-333-3333"
    lead_source = '50378'


class BaseMixinPPE(BaseMixinPP):
    move_in_years = ['2018', '2019']
    contact_url_t = '{}/#contact'


class PPBaseParseSpider(BaseParseSpider, BaseMixinPP):
    phone_x = '//div[contains(@class, "new-contact-details") and contains(.,"Phone")]/p//text()'
    email_x = '//div[contains(@class, "new-contact-details") and contains(.,"Email")]/p//text()'
    description_x = '//*[@id="overview"]/div/div[1]//text()[not(ancestor::div[@class="directions-block"])]'

    floor_availability_t = ('{}/Apartments/module/application_unit_info/floorplan_availability_filter[is_submit]/1/'
                            '/show_all/1/?application[lease_start_date]={date}&is_from_navigation_button=0&floorplan'
                            '_availability_filter%5Bis_submit%5D=1&is_floorplan_availability_filter_submit=1&'
                            'application%5Blease_start_date%5D={date}&captcha_verified=false')

    unit_list_url_t = ('{}/Apartments/module/application_unit_info/action/view_unit_spaces/floorplan_'
                       'availability_filter[is_submit]/1//property_floorplan[id]/{}/?application[lease_start_date]={}')

    unit_details_url_t = ('{}/Apartments/module/application_unit_info/action/view_unit_details/floorplan_'
                          'availability_filter[is_submit]/1//property_floorplan[id]/{}/unit_space[id]/{}/'
                          '?application[lease_start_date]={}')

    price_url_t = ('{}/Apartments/module/application_system/action/reload_scheduled_charges/show_rates/1'
                   '/application[id]/{}')

    submit_room_price_form = {
        'is_from_navigation_button': '0',
        'floorplan_availability_filter[is_submit]': '1',
        'is_floorplan_availability_filter_submit': '1',
        'application[term_month]': '12',
        'application[lease_term_id]': '1251',
        'captcha_verified': 'false',
    }

    contact_info = []
    p_amenities = []
    p_images = []
    r_photos = []
    r_amenities = []
    deals = []
    p_desc = []

    def parse(self, response):
        return_url = self.price_url_t.format(self.login_domain, response.meta['application_id'])
        self.submit_room_price_form['application[lease_start_date]'] = self.move_in_date()
        self.submit_room_price_form['return_url'] = return_url
        url = self.floor_availability_t.format(self.login_domain, date=self.move_in_date())
        return Request(url, self.parse_floor_availability)

    def parse_floor_availability(self, response):
        floor_s = response.css('.js-select-row')
        for f_s in floor_s:
            floor_id = clean(f_s.css('[data-floorplan]::attr(data-floorplan)'))
            if not floor_id:
                continue

            raw_prices = clean(f_s.css('.col-fp.rent::text'))
            price = self.clean_prices(raw_prices)
            raw_deposit = clean(f_s.css('.col-fp.deposit::text'))
            deposit = self.clean_prices(raw_deposit)
            apartment_name = clean(f_s.css('.js-space-name::text'))[0]

            floor_plans = clean(f_s.css('.fp-layout-link::attr(href)'))
            floor_plans = [response.urljoin(u) for u in floor_plans]
            meta = {
                'floor_plans': floor_plans,
                'price': price,
                'deposit': deposit,
                'apartment_name': apartment_name}

            url = self.unit_list_url_t.format(self.login_domain, floor_id[0], self.move_in_date())
            yield Request(url, self.parse_unit_list, meta=meta)

    def parse_unit_list(self, response):
        floor_plans = response.meta['floor_plans']

        for unit_s in response.css('.row-unit '):
            loader = RoomLoader(item=Room(), selector=unit_s, date_format='%m/%d/%Y')
            loader.add_value('listing_type', 'flexible_open_end')
            loader.add_value('property_name', self.property_name)
            loader.add_value('property_url', self.site_domain)
            loader.add_value('floor_plans', floor_plans)
            loader.add_value('property_slug', self.property_slug)
            loader.add_value('room_photos', self.r_photos)
            loader.add_value('room_name', self.room_name(unit_s, response))
            loader.add_value('room_amenities', self.r_amenities)
            loader.add_css('room_amenities', '.unit-add-info li:not(:first-child) ::text')
            loader.add_value('property_amenities', self.p_amenities)
            loader.add_value('property_description', self.p_desc)
            loader.add_value('property_contact_info', self.contact_info)
            loader.add_value('property_images', self.p_images)
            loader.add_value('available_from', self.move_in_date())
            loader.add_value('deals', self.deals)
            loader.add_value('room_price', self.room_price(unit_s, response))
            loader.add_value('deposit_amount', self.deposit_amount(unit_s, response))
            loader.add_value('deposit_type', 'fixed')
            item = loader.load_item()
            meta = {
                'item': item
            }
            floor_id = unit_s.css('a::attr(data-floorplan)').extract_first()
            unit_id = unit_s.css('a::attr(data-unit)').extract_first()
            url = self.unit_details_url_t.format(self.login_domain, floor_id, unit_id, self.move_in_date())
            yield Request(url, self.parse_min_duration, meta=meta.copy())

    def parse_min_duration(self, response):
        item = response.meta['item']

        for lease_s in response.css('li[data-term]'):
            loader = RoomLoader(item=item, min_duration_format='months', selector=lease_s)
            loader.add_xpath('min_duration', './@data-term')
            yield loader.load_item()

    def room_name(self, sel, response):
        apartment_name = response.meta['apartment_name']
        name = clean(sel.css('.unit-select::text'))
        return clean(f"{apartment_name}-{name[0]}")

    def room_price(self, sel, response):
        price = response.meta['price']
        raw_prices = clean(sel.css('.rent .unit-detail::text'))
        return self.clean_prices(raw_prices) or price

    def deposit_amount(self, sel, response):
        price = response.meta['deposit']
        raw_prices = clean(sel.css('.deposit .unit-detail::text'))
        return self.clean_prices(raw_prices) or price

    def clean_prices(self, raw_prices):
        prices = re.findall('(\$\d+)', "".join(raw_prices))
        return prices[0] if prices else ''

    def move_in_date(self):
        return datetime.today().strftime('%m/%d/%Y')


class PPBaseParseSpiderE(PPBaseParseSpider, BaseMixinPPE):
    phone_x = '//div[contains(@class, "new-contact-details") and contains(.,"Phone")]/p//text()'
    email_x = '//div[contains(@class, "new-contact-details") and contains(.,"Email")]/p//text()'
    description_x = '//*[@id="overview"]/div/div[1]//text()[not(ancestor::div[@class="directions-block"])]'

    room_url_t = ('{}/Apartments/module/application_unit_info/action/view_floorplans_for_student/application'
                  '[lease_start_window_id]/{}/is_immediate_movein_lease_term/false')
    room_url_i_t = ('{}/Apartments/module/application_unit_info/action/view_floorplans_for_student/application'
                    '[lease_start_window_id]/{}/immediate_movein_date/{}/is_immediate_movein_lease_term/true')

    set_info_url_t = '{}/Apartments/module/application_unit_info/action/insert_floorplan_info_for_student/'

    room_price_url_t = ('{}/Apartments/module/application_system/action/reload_scheduled_charges/show_rates/1/'
                        'application\[id\]/{}')

    room_rent_x = '//span[contains(@title, "Rent")]/parent::div/following-sibling::div//text()'

    details_css = '.room-row:not(.header)'

    room_price_css = '.monthly-col::text'

    requests_queue = []

    def parse(self, response):
        app_id = response.css('footer+script').re_first('"app_id":"(\d+)",')
        for m_s in response.css('#lease_start_window_id li'):
            raw_date = clean(m_s.css('input::attr(data-move-in)'))
            if not raw_date:
                continue

            term_dates = clean(m_s.css(' ::text'))
            in_date, out_date = re.findall('(\d{2}\/\d{2}\/\d{4})', term_dates[0])
            m_value = clean(m_s.css(' ::attr(value)'))[0]
            url = self.room_url_t.format(self.login_domain, m_value)

            current_date = datetime.now().date()
            dt = datetime.strptime(raw_date[0], '%m/%d/%Y')

            if current_date >= dt.date():
                url = self.room_url_i_t.format(self.login_domain, m_value, current_date.strftime('%m-%d-%Y'))
            meta = {
                'move_in_date': in_date, 'move_out_date': out_date, 'lease_id': m_value, 'app_id': app_id
            }
            req = Request(url, callback=self.parse_rooms, meta=meta.copy())
            self.requests_queue.append(req)

    def parse_rooms(self, response):
        loader_c = RoomLoader(item=Room(), selector=response, date_format='%m/%d/%Y')
        loader_c.add_value('move_in_date', response.meta['move_in_date'])
        loader_c.add_value('move_out_date', response.meta['move_out_date'])
        loader_c.add_value('property_images', self.p_images)
        loader_c.add_value('property_amenities', self.p_amenities)
        loader_c.add_value('property_description', self.p_desc)
        loader_c.add_value('property_contact_info', self.contact_info)
        loader_c.add_value('property_name', self.property_name)
        loader_c.add_value('property_url', self.site_domain)
        loader_c.add_value('room_availability', 'Available')
        loader_c.add_value('deals', self.deals)
        common_item = loader_c.load_item()

        for r_s in response.css('#floorplan-overview-content .list-item'):
            loader = RoomLoader(item=common_item.copy(), selector=r_s, floor_images_domain=self.login_domain)
            loader.add_value('room_amenities', self.r_amenities)
            loader.add_value('room_photos', self.r_photos)
            loader.add_css('room_amenities', '.sub-title ::text')
            loader.add_css('floor_plans', '.layout ::attr(src)', self.clean_floor_plan)
            loader.add_css('room_name', '.title ::text')
            yield from self.room_types(response, r_s, loader.load_item())

    def room_types(self, response, room_s, common_room):

        for r_s in room_s.css(self.details_css):
            loader = RoomLoader(item=common_room.copy(), selector=r_s)
            room_name = self.room_name(response, room_s, r_s)

            if self.is_room_valid(response, room_s, r_s):
                loader.add_value("property_slug", self.property_slug)
                loader.replace_value('room_name', room_name)
                loader.add_css('room_type', '.type-col ::text', self.clean_deposit_price)
                loader.add_css('room_price', self.room_price_css, self.clean_room_price)
                price = loader.get_output_value('room_price')
                item = loader.load_item()

                if price:
                    yield item
                    continue

                meta = {
                    'item': item, 'app_id': response.meta['app_id']
                }
                url = self.set_info_url_t.format(self.login_domain)
                data = self.form_data(response.meta['lease_id'], r_s)
                req = FormRequest(url=url, method='POST', meta=meta.copy(), formdata=data,
                                  callback=self.price_request, dont_filter=True)

                self.requests_queue.append(req)

    def price_request(self, response):
        url = self.room_price_url_t.format(self.login_domain, response.meta['app_id'])
        meta = {'item': response.meta['item']}

        yield Request(url=url, callback=self.parse_room_price, meta=meta.copy(), dont_filter=True)

    def parse_room_price(self, response):
        item = response.meta['item']
        loader = RoomLoader(item=item, response=response)
        loader.add_css('deals', 'span[title*=Discount]::text')
        loader.add_value('deals', item.get('deals', ''))
        loader.add_xpath('room_price', self.room_rent_x, self.clean_room_price)
        yield loader.load_item()

    def form_data(self, lease_id, room_s):
        floor_plan_id = room_s.css('input::attr(value)').extract_first()
        space_configuration_id = room_s.css('input::attr(space_config_val)').extract_first()
        data = {
            'application[space_configuration_id]': space_configuration_id,
            'application[lease_start_window_id]': lease_id,
            'application[property_floorplan_id]': floor_plan_id
        }

        return data

    def clean_floor_plan(self, floor_plans):
        return [f_p for f_p in floor_plans if "comming_soon" not in f_p]

    def is_room_valid(self, response, room_s, r_s):
        return True

    def room_name(self, response, c_sel, sel):
        return ''

    def clean_room_price(self, prices):
        prices = ['-'.join(re.findall('\$\s*[\d,]+', p)) for p in prices]
        return [p.replace(',', '') for p in prices]

    def clean_deposit_price(self, prices):
        return prices


class PPBaseCrawlSpider(BaseCrawlSpider, BaseMixinPP):
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'
    }
    contact_info_css = '.visit-info::text'
    p_amenities_css = '.field-item ul ::text'
    p_images_css = '.view-amenities-gallery img ::attr(src)'
    r_amenities_css = '.view-unit-features ul ::text'
    r_photos_css = ''

    def start_requests(self):
        url = self.contact_url_t.format(self.site_domain)
        yield Request(url, self.parse_contact, priority=1)
        url = self.amenities_url_t.format(self.site_domain)
        yield Request(url, self.parse_amenities, priority=1)
        url = self.floor_amenities_url_t.format(self.site_domain)
        yield Request(url, self.parse_floor_amenities, priority=1)
        url = self.login_url_t.format(self.login_domain)
        yield Request(url, self.parse_login_page)

    def parse_contact(self, response):
        self.parse_spider.contact_info += clean(response.css(self.contact_info_css))

    def parse_amenities(self, response):
        ps = self.parse_spider
        ps.p_amenities += clean(response.css(self.p_amenities_css))
        ps.p_images += clean(response.css(self.p_images_css))

    def parse_floor_amenities(self, response):
        ps = self.parse_spider
        ps.r_amenities += clean(response.css(self.r_amenities_css))
        if self.r_photos_css:
            ps.r_photos += clean(response.css(self.r_photos_css))

    def parse_login_page(self, response):
        login_url = response.css('#returning_applicants_login::attr(action)').extract_first()
        data = {
            'applicant[username]': self.login_email,
            'applicant[password]': self.login_password,
            'returning_applicant': '1',
        }
        return FormRequest(login_url, formdata=data, callback=self.parse_login, dont_filter=True)

    def parse_login(self, response):
        url = response.css('.btn.js-app-nav::attr(href)').extract_first()
        if url != '#':
            return Request(url, self.parse, dont_filter=True)
        url = self.login_url_t.format(self.login_domain)
        return Request(url, self.parse_signup, dont_filter=True)

    def parse(self, response):
        application_id_href = clean(response.css(".legal-link-list .legal-link ::attr(href)"))[0]
        application_id = re.findall('application\[id\]=(\d+)', application_id_href)[0]
        yield Request(self.unit_info_url_t.format(self.login_domain),
                      callback=self.parse_spider.parse, dont_filter=True,
                      meta={'application_id': application_id})

    def parse_signup(self, response):
        signup_url = clean(response.css("#create_applicant ::attr(action)"))[0]
        form_data = {
            'application[company_application_id]': clean(
                response.css('#default_company_application_id ::attr(value)'))[0],
            'show_terms_and_conditions': '1',
            'applicant[customer_relationship_id]': clean(
                response.css('#customer_relationship_id_hidden ::attr(value)'))[0],
            'applicant[name_first]': self.first_name,
            'applicant[name_last]': self.last_name,
            'applicant[primary_phone_number]': self.phone_num,
            'applicant[primary_phone_number_type_id]': '4',
            'application[validate_secondary_phone_number]': '0',
            'applicant[secondary_phone_number]': '',
            'applicant[secondary_phone_number_type_id]': '2',
            'applicant[username]': self.login_email,
            'applicant[password]': self.login_password,
            'applicant[password_confirm]': self.login_password,
            'application[validate_lead_source]': clean(response.css('#validate_lead_source ::attr(value)'))[0],
            'application[lead_source_id]': self.lead_source,
            'application[is_lead_source_hidden]': clean(
                response.css('#is_application_lead_source_hidden ::attr(value)'))[0],
            'application[desired_movein_date]': clean(
                response.xpath('//input[@name="application[desired_movein_date]"]/@value'))[0],
            'agrees_to_terms': clean(response.css('#agrees_to_terms ::attr(value)'))[0],
            'is_new_applicant': '1'
        }
        return FormRequest(url=signup_url, formdata=form_data, callback=self.parse)


class PPBaseCrawlSpiderE(PPBaseCrawlSpider, BaseMixinPPE):
    contact_info_css = '.pane-node-field-phone-number::text'
    p_amenities_css = '.pane-amenities-list ::text'
    p_images_css = '.photoswipe-gallery a::attr(href)'
    r_amenities_css = '.unit-features-list ::text'
    r_photos_css = '.photoswipe-gallery a::attr(href)'
    deal_x = '//*[contains(@class, "field-collection-view") and contains(., "Summer Specials")]//section//text()'

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(PPBaseCrawlSpiderE, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.request_from_queue, signal=signals.spider_idle)
        return spider

    def request_from_queue(self, spider):
        ps = self.parse_spider

        if ps.requests_queue:
            self.crawler.engine.crawl(ps.requests_queue.pop(), self)

    def parse_floor_amenities(self, response):
        super().parse_floor_amenities(response)
        ps = self.parse_spider
        ps.deals += clean(response.xpath(self.deal_x))
