# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from NWHScrapper.items import NwhscrapperItem


class NWHSpider(scrapy.Spider):
    name = 'nwhspider'
    allowed_domains = ['www.nwh.org']
    start_urls = ['https://www.nwh.org/find-a-doctor/find-a-doctor-home']

    def parse(self, response):
        # create request to get all doctors
        data = {
            '__EVENTTARGET': 'ctl00$cphContent$ctl01$lnkSeachResults',
            'ctl00$cphContent$ctl01$ddlResultsPerPage': '99999',
        }

        url = 'https://www.nwh.org/find-a-doctor/find-a-doctor-home?type=1'
        print("Loading all doctors")
        yield scrapy.FormRequest(url=url, method='POST', formdata=data, callback=self.parse_doctors)

    def parse_profile(self, response):
        doctor = NwhscrapperItem()

        doctor['source_url'] = response.url
        full_name = "div.pnl-doctor-name>h1::text"
        doctor['full_name'] = response.css(full_name).extract_first()
        address = "div[id *= 'Residency']>ul>li::text"
        doctor['address'] = response.css(address).extract_first()
        speciality = "div.pnl-doctor-specialty>h2::text"  # strip
        doctor['speciality'] = response.css(speciality).extract_first().strip()
        image_url = "div.pnl-doctor-image>img::attr(src)"  # response.urljoin
        doctor['image_url'] = response.css(image_url).extract_first()
        affiliation = "div[id *= 'Fellowship']>ul>li::text"
        doctor['affiliation'] = response.css(affiliation).extract_first()
        medical_school = "div[id *= 'MedicalSchool']>ul>li::text"
        doctor['medical_school'] = response.css(medical_school).extract_first()
        graduate_education = "div[id *= 'Certifications']>ul>li::text"
        doctor['graduate_education'] = response.css(graduate_education).extract_first()
        doctor['crawled_date'] = datetime.now()

        yield doctor

    def get_profile_ids(self, response):
        profile_ids = "div.search-results-physician>input::attr(value)"
        return response.css(profile_ids).extract()

    def make_profile_urls(self, response):
        profile_urls = []
        profile_ids = self.get_profile_ids(response)
        print("ids: "+str(len(profile_ids)))
        base_url = "https://www.nwh.org/find-a-doctor/find-a-doctor-profile"
        for profile_id in profile_ids:
            profile_url = base_url + "?id=" + str(profile_id)
            profile_urls.append(profile_url)
        return profile_urls

    def parse_doctors(self, response):
        # retrieve list of all profile links
        profile_urls = self.make_profile_urls(response)
        # yield requests to parse each profile
        for profile_url in profile_urls:
            yield scrapy.Request(profile_url,
                                 callback=self.parse_profile,
                                 dont_filter=True,)