from datetime import datetime

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Compose
from scrapy.loader.processors import MapCompose
from scrapy.loader.processors import Join
from scrapy.loader.processors import TakeFirst

BASE_URL = 'https://www.nwh.org/find-a-doctor/'


class DoctorItem(scrapy.Item):
    full_name = scrapy.Field()
    specialty = scrapy.Field()
    image_url = scrapy.Field()
    source_url = scrapy.Field()
    graduate_education = scrapy.Field()
    crawled_date = scrapy.Field(serializer=str)
    medical_school = scrapy.Field()
    affiliation = scrapy.Field()
    address = scrapy.Field()


class AddressItem(scrapy.Item):
    phone = scrapy.Field()
    fax = scrapy.Field()
    other = scrapy.Field()


def strip(value):
    return value.strip()


map_strip = MapCompose(strip)
clean_text = Compose(map_strip, Join(), strip)
name_dict = MapCompose(lambda name: {'name': name})


class DoctorItemLoader(ItemLoader):
    default_item_class = DoctorItem
    full_name_out = TakeFirst()
    specialty_out = Compose(TakeFirst(), lambda str: str.split(','), map_strip)
    image_url_out = TakeFirst()
    source_url_out = TakeFirst()
    crawled_date_out = TakeFirst()
    graduate_education_out = MapCompose(
        lambda name: {'type': 'Residency', 'name': name})
    medical_school_out = name_dict
    affiliation_out = name_dict
    address = scrapy.Field()


class AddressItemLoader(ItemLoader):
    default_item_class = AddressItem
    phone_out = clean_text
    fax_out = clean_text


class NWHSpider(scrapy.Spider):
    name = 'nwh'

    def start_requests(self):
        formdata = {
            '__EVENTTARGET': 'ctl00$cphContent$ctl01$lnkSeachResults',
            'ctl00$cphContent$ctl01$ddlResultsPerPage': '99999'
        }

        url = "{}ContentPage.aspx?nd=847".format(BASE_URL)
        yield scrapy.FormRequest(url, callback=self.parse, formdata=formdata)

    def parse(self, response):
        ids = response.css(
            '.search-results-physician>input::attr(value)').extract()

        self.log('{} doctors found'.format(len(ids)))

        for id in ids:
            url = '{}find-a-doctor-profile?id={}'.format(BASE_URL, id)
            yield scrapy.Request(url=url, callback=self.parse_doctor)

    def parse_doctor(self, response):
        profile = response.css('.find-a-doc-profile-wrapper')

        loader = DoctorItemLoader(selector=profile)
        loader.add_value('crawled_date', datetime.now())
        loader.add_css('full_name', '.header-doctor-name::text')
        loader.add_css('specialty', '.pnl-doctor-specialty>h2::text')
        loader.add_value('source_url', response.request.url)
        loader.add_value('image_url', response.urljoin(profile.css(
            '.pnl-doctor-image>img::attr(src)').extract_first()))
        loader.add_css('graduate_education',
                       '#ctl00_cphContent_ctl01_pnlResidency li::text')
        loader.add_css('medical_school',
                       '#ctl00_cphContent_ctl01_pnlMedicalSchool li::text')
        loader.add_css('affiliation',
                       '.doctor-contact-location-name span:last-child::text')

        for info in profile.css('.pnl-doctor-contact-location'):
            addressloader = AddressItemLoader(selector=info)
            addressloader.add_css('phone', '.doc-phone::text')
            addressloader.add_css('fax', '.doc-fax::text')
            addressloader.add_css(
                'other', '.doctor-contact-location-address>a:last-child::text')
            loader.add_value('address', dict(addressloader.load_item()))

        return loader.load_item()
