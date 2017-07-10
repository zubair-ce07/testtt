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
            doctor_id = doctor_profile.xpath('./input[contains(@id, "PhysicianID")]/@value').extract_first()
            doctor_id_key = doctor_profile.xpath('./input[contains(@id, "PhysicianID")]/@name').extract_first()
            viewprofile_wrapper = doctor_profile.xpath('.//div[@class="view-profile-wrapper"]').pop()
            viewprofile_key = viewprofile_wrapper.xpath('./input[@value="View Full Profile"]/@name').extract_first()
            yield FormRequest(url, method='POST', formdata={doctor_id_key: doctor_id,
                                                            viewprofile_key: 'View Full Profile',
                                                            '__VIEWSTATE': viewstate},
                              callback=self.parse_doctor_profile)

    def get_graduation_info(self, response):
        graduate_education = []
        residency = {'type': 'Residency',
                     'name': response.xpath('//div[contains(@id, "pnlResidency")]//li//text()').extract()}
        fellowship = {'type': 'Fellowship',
                      'name': response.xpath('//div[contains(@id, "pnlFellowship")]//li//text()').extract()}
        graduate_education.append(residency)
        graduate_education.append(fellowship)
        return graduate_education

    def get_address_info(self, response):
        phone = response.xpath('//span[contains(@id, "lblDocContactPhone")]//text()').extract_first()
        fax = response.xpath('//span[contains(@id, "lblDocContactFax")]//text()').extract_first()
        other = response.css('div.doctor-contact-location-address a::text').extract()
        address = {'phone': phone, 'fax': fax, 'other': other}
        return address

    def parse_doctor_profile(self, response):
        doctor_item_loader = DoctorItemLoader(item=DoctorItem(), response=response)
        doctor_item_loader.add_value('crawled_date', str(datetime.now()))
        doctor_item_loader.add_value('source_url', response.url)
        speciality = response.xpath('//div[contains(@id, "pnlDocSpecialty")]/h2//text()').extract_first()
        doctor_item_loader.add_value('speciality', speciality)
        image_url = response.xpath('//div[contains(@id, "pnlDoctorImage")]/img/@src').extract_first()
        doctor_item_loader.add_value('image_url', image_url)
        full_name = response.xpath('//div[contains(@id, "pnlDocName")]/h1//text()').extract_first()
        doctor_item_loader.add_value('full_name', full_name)
        address = self.get_address_info(response)
        doctor_item_loader.add_value('address', address)
        medical_school = response.xpath('//div[contains(@id, "pnlMedicalSchool")]//li//text()').extract()
        doctor_item_loader.add_value('medical_school', medical_school)
        affiliation = {'name': response.xpath('//div[contains(@id, "pnlInternship")]//li//text()').extract()}
        doctor_item_loader.add_value('affiliation', affiliation)
        graduate_education = self.get_graduation_info(response)
        doctor_item_loader.add_value('graduate_education', graduate_education)
        return doctor_item_loader.load_item()
