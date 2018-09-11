from datetime import datetime

import scrapy
from NWH.items import NwhLoader


class NwhSpider(scrapy.Spider):
    name = "nwh"

    def start_requests(self):
        return [scrapy.FormRequest("https://www.nwh.org/find-a-doctor/ContentPage.aspx?nd=847",
                                   formdata={'__EVENTTARGET': 'ctl00$cphContent$ctl01$lnkSeachResults',
                                             'ctl00$cphContent$ctl01$ddlResultsPerPage': '99999'}, callback=self.parse)]

    def parse(self, response):
        doctors_id = response.xpath('//div[@class="search-results-physician"]/input/@value').extract()
        for doctor_id in doctors_id:
            yield scrapy.Request("https://www.nwh.org/find-a-doctor/find-a-doctor-profile?id={}".format(doctor_id), callback=self.parse_item)

    def parse_item(self, response):
        loader = NwhLoader(response=response)
        loader.add_value("crawled_date", str(datetime.now()))
        loader.add_value('source_url', response.url)
        loader.add_xpath("full_name", '//h1[@class="header-doctor-name"]/text()')
        loader.add_xpath("speciality", '//div[@id="ctl00_cphContent_ctl01_pnlDocSpecialty"]/h2/text()')
        loader.add_xpath("medical_school", '//div[@id="ctl00_cphContent_ctl01_pnlMedicalSchool"]/ul/li/text()')
        loader.add_xpath("address", '//div[@class="doctor-contact-location-address clearfix"]/a[1]/text()')
        loader.add_xpath("affiliation", '//div[@id="ctl00_cphContent_ctl01_pnlFellowship"]/ul/li/text()')
        loader.add_xpath("graduate_education", '//div[@id="ctl00_cphContent_ctl01_pnlBoardOfCertifications"]/ul/li/text()')
        loader.add_xpath("image_url", '//div[@id="ctl00_cphContent_ctl01_pnlDoctorImage"]/img/@src')
        return loader.load_item()
