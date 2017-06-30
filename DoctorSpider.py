import scrapy
from scrapy.http import FormRequest
from scrapy.loader import ItemLoader
from FindADoctor.items import DoctorItem
from datetime import datetime


class DoctorSpider(scrapy.Spider):
    name = "doctor_spider"
    start_urls = ["https://www.nwh.org/find-a-doctor/ContentPage.aspx?nd=847&type=1"]

    def parse(self, response):
        url = self.start_urls[0]
        viewstate = response.xpath('//input[@id = "__VIEWSTATE"]/@value').extract_first()
        yield FormRequest(url, method='POST',
                          formdata={'ctl00$cphContent$ctl01$ddlResultsPerPage': '99999', '__VIEWSTATE': viewstate},
                          callback=self.generator_viewprofile_request)

    def generate_viewprofile_request(self, response):
        doctor_ids = response.xpath('//div[@class="search-results-physician"]/input[@type = "hidden"]/@value').extract()
        physicianid_keys = response.xpath('//div[@class="search-results-physician"]/input[@type = "hidden"]/@name').extract()
        viewprofile_keys = response.xpath('//div[@class="view-profile-wrapper"]/input[@type = "submit"]/@name').extract()
        viewstate = response.xpath('//input[@id = "__VIEWSTATE"]/@value').extract_first()
        url = self.start_urls[0]
        for index in range(0, len(doctor_ids)):
            id = (doctor_ids[index])
            physicianid_key = physicianid_keys[index]
            viewprofile_key = viewprofile_keys[index]
            yield FormRequest(url, method='POST', formdata={physicianid_key: id, viewprofile_key: 'View Full Profile', '__VIEWSTATE': viewstate}, callback=self.extract_doctor_profile_info)

    def get_graduation_info(self, response):
        graduate_education = []
        residency = {'type': 'Residency', 'name': response.css('div#ctl00_cphContent_ctl01_pnlResidency li::text').extract()}
        fellowship = {'type': 'Fellowship', 'name': response.css('div#ctl00_cphContent_ctl01_pnlFellowship li::text').extract()}
        graduate_education.append(residency)
        graduate_education.append(fellowship)
        return graduate_education

    def get_address_info(self, response):
        phone = response.css('span#ctl00_cphContent_ctl01_lblDocContactPhone::text').extract_first()
        fax = response.css('span#ctl00_cphContent_ctl01_lblDocContactFax::text').extract_first()
        other = response.css('div.doctor-contact-location-address a::text').extract()
        address = {'phone': phone, 'fax': fax, 'other': other}
        return address

    def extract_doctor_profile_info(self, response):
        l = ItemLoader(item=DoctorItem(), response=response)
        l.add_value('crawled_date', str(datetime.now()))
        l.add_value('source_url', response.url)
        l.add_css('speciality', 'div#ctl00_cphContent_ctl01_pnlDocSpecialty h2::text')
        l.add_css('image_url', 'div#ctl00_cphContent_ctl01_pnlDoctorImage img::attr(src)')
        l.add_css('full_name', 'div#ctl00_cphContent_ctl01_pnlDocName h1::text')
        address = self.get_address_info(response)
        l.add_value('address', address)
        l.add_css('medical_school', 'div#ctl00_cphContent_ctl01_pnlMedicalSchool li::text')
        affiliation = {'name': response.css('div#ctl00_cphContent_ctl01_pnlInternship li::text').extract()}
        l.add_value('affiliation', affiliation)
        graduate_education = self.get_graduation_info(response)
        l.add_value('graduate_education', graduate_education)
        return l.load_item()
