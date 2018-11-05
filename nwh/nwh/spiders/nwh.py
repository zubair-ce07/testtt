"""
This module crawls pages and gets data.
"""
import re
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import scrapy
from ..items import Product


class Nwh(CrawlSpider):
    """This class crawls Nwh pages"""
    name = 'nwh'
    allowed_domains = ['nwh.org']
    start_urls = ['https://www.nwh.org/']
    rules = [
        Rule(LinkExtractor(
            allow=(r'https://www.nwh.org/find-a-doctor/find-a-doctor-home')),
             callback='parse_doctor'),
    ]

    def parse_doctor(self, response):
        """This method crawls page urls."""
        formdata = {'__EVENTTARGET': 'ctl00$cphContent$ctl01$lnkSeachResults',
                    'ctl00$cphContent$ctl01$ddlResultsPerPage': '99999'}
        yield scrapy.FormRequest(response.url, formdata=formdata,\
         callback=self.parse_doctor_profile)

    def parse_doctor_profile(self, response):
        """This method crawls doctor profile urls."""
        profile_values = []
        profile_url = re.split('home', response.url)[0] + 'profile?id='
        for doc in response.css('div>div.search-results-physician'):
            value = doc.css('.search-results-physician>input::attr(value)').extract_first()
            profile_values.append(value)
        for data in profile_values:
            detail_url = profile_url + str(data)
            yield scrapy.Request(detail_url, callback=self.parse_doctor_detail)

    def parse_doctor_detail(self, response):
        """This method crawls details of doctor."""
        speciality = response.css(
            '.pnl-doctor-specialty>h2::text').extract_first().strip()
        source_url = response.url
        affiliation = response.css(
            '#ctl00_cphContent_ctl01_pnlBoardOfCertifications >ul>li::text').extract_first()
        medical_school = response.css(
            '#ctl00_cphContent_ctl01_pnlMedicalSchool>ul>li::text').extract_first()
        image_url = response.css(
            '#ctl00_cphContent_ctl01_imgDoctorImage::attr(src)').extract_first()
        full_name = response.css('.pnl-doctor-name>h1::text').extract_first()
        address = response.css(
            ' div.doctor-contact-location-address.clearfix>a::text').extract()

        loader = ItemLoader(item=Product(), response=response)
        loader.add_value('speciality', speciality)
        loader.add_value('source_url', source_url)
        loader.add_value('affiliation', affiliation)
        loader.add_value(
            'medical_school', medical_school)
        loader.add_value(
            'image_url', image_url)
        loader.add_value('full_name', full_name)
        loader.add_value('address', address)
        return loader.load_item()
