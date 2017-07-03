import scrapy
from scrapy.http import FormRequest
from FindADoctor.items import DoctorItem, DoctorItemLoader
from datetime import datetime


class DoctorSpider(scrapy.Spider):
    name = "doctor_spider"
    start_urls = ["https://www.nwh.org/find-a-doctor/ContentPage.aspx?nd=847&type=1"]

    def parse(self, response):
        url = self.start_urls[0]
        viewstate = response.xpath('//input[@id = "__VIEWSTATE"]/@value').extract_first()
        yield FormRequest(url, method='POST',
                          formdata={'ctl00$cphContent$ctl01$ddlResultsPerPage': '99999', '__VIEWSTATE': viewstate},
                          callback=self.generate_viewprofile_request)

    def generate_viewprofile_request(self, response):
        url = self.start_urls[0]
        viewstate = response.xpath('//input[@id = "__VIEWSTATE"]/@value').extract_first()
        doctor_profiles_selector = response.xpath('//div[@class="search-results-physician"]')
        for doctor_profile in doctor_profiles_selector:
            doctor_id = doctor_profile.xpath('./input[@type = "hidden"]/@value').extract_first()
            doctor_id_key = doctor_profile.xpath('./input[@type = "hidden"]/@name').extract_first()
            viewprofile_key = doctor_profile.xpath('./div[@class="row"]/div[@class="search-results-physician-info col-md-10"]/div[@class="search-results-physician-info-inner"]/div[@class="physician-info row"]/section/div[@class="view-profile-wrapper"]/input[@type = "submit"]/@name').extract_first()
            yield FormRequest(url, method='POST', formdata={doctor_id_key: doctor_id, viewprofile_key: 'View Full Profile', '__VIEWSTATE': viewstate}, callback=self.parse_doctor_profile)

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

    def parse_doctor_profile(self, response):
        doctor_item_loader = DoctorItemLoader(item=DoctorItem(), response=response)
        doctor_item_loader.add_value('crawled_date', str(datetime.now()))
        doctor_item_loader.add_value('source_url', response.url)
        doctor_item_loader.add_css('speciality', 'div#ctl00_cphContent_ctl01_pnlDocSpecialty h2::text')
        doctor_item_loader.add_css('image_url', 'div#ctl00_cphContent_ctl01_pnlDoctorImage img::attr(src)')
        doctor_item_loader.add_css('full_name', 'div#ctl00_cphContent_ctl01_pnlDocName h1::text')
        address = self.get_address_info(response)
        doctor_item_loader.add_value('address', address)
        doctor_item_loader.add_css('medical_school', 'div#ctl00_cphContent_ctl01_pnlMedicalSchool li::text')
        affiliation = {'name': response.css('div#ctl00_cphContent_ctl01_pnlInternship li::text').extract()}
        doctor_item_loader.add_value('affiliation', affiliation)
        graduate_education = self.get_graduation_info(response)
        doctor_item_loader.add_value('graduate_education', graduate_education)
        return doctor_item_loader.load_item()
