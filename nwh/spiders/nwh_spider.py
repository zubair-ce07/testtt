from datetime import datetime
from urllib.parse import urljoin

import scrapy

from nwh.loaders import DoctorItemLoader
from nwh.loaders import AddressItemLoader


BASE_URL = 'https://www.nwh.org/find-a-doctor/'


class NWHSpider(scrapy.Spider):
    name = 'nwh_spider'

    def start_requests(self):
        formdata = {
            '__EVENTTARGET': 'ctl00$cphContent$ctl01$lnkSeachResults',
            'ctl00$cphContent$ctl01$ddlResultsPerPage': '99999'
        }

        url = urljoin(BASE_URL, 'ContentPage.aspx?nd=847')
        yield scrapy.FormRequest(url, callback=self.parse, formdata=formdata)

    def parse(self, response):
        ids = response.css(
            '.search-results-physician>input::attr(value)').extract()

        self.log('{} doctors found'.format(len(ids)))

        for id in ids:
            url = urljoin(BASE_URL, 'find-a-doctor-profile?id={}'.format(id))
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

        addresses = self.parse_addresses(
            profile.css('.pnl-doctor-contact-location'))
        loader.add_value('address', addresses)

        return loader.load_item()

    def parse_addresses(self, selectors):
        addresses = []
        for info in selectors:
            addressloader = AddressItemLoader(selector=info)
            addressloader.add_css('phone', '.doc-phone::text')
            addressloader.add_css('fax', '.doc-fax::text')
            addressloader.add_css(
                'other', '.doctor-contact-location-address>a:last-child::text')
            addresses.append(dict(addressloader.load_item()))
        return addresses
