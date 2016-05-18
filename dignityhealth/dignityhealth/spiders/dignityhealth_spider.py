import datetime
import json
import scrapy
import string
import itertools
from scrapy.http import Request
from scrapy.http import FormRequest
from dignityhealth.items import DoctorProfile
from scrapy.selector import Selector


class DignityHealthSpider(scrapy.Spider):
    name = "dignityhealth_spider"
    allowed_domains = ["dignityhealth.org"]
    start_urls = ['http://www.dignityhealth.org/stmarymedical/find-a-doctor']
    search_params = ''

    def parse(self, response):
        self.get_search_parameters(response)
        yield self.send_next_search_request(response)

    def send_next_search_request(self, response):
        params = self.get_next_search_params()
        if params:
            return FormRequest.from_response(
                response,
                formdata={'FindADoctorSearch$DropDownList_State$HiddenField_Value': params[0],
                          'FindADoctorSearch$DropDownList_Distance$HiddenField_Value': '100',
                          'FindADoctorSearch$TextBox_City_Real': params[1]},
                formxpath='//form[@id="form1"]',
                dont_click=True,
                url='http://www.dignityhealth.org/stmarymedical/WF_FindADoc_Results.aspx',
                callback=self.parse_doctor_profiles)

    def get_search_parameters(self, response):
        states = response.xpath('//div[@id="FindADoctorSearch_DropDownList_State__Panel_List_Items"]'
                                '//div/text()').extract()[1:]
        cities = list(string.lowercase)
        self.search_params = list(itertools.product(states, cities))

    def get_next_search_params(self):
        if self.search_params:
            return self.search_params.pop(0)

    def parse_doctor_profiles(self, response):
        base_url = "http://www.dignityhealth.org/stmarymedical/WF_FindADoc_Profile.aspx?id="
        current_page = response.meta['page'] if 'page' in response.meta else 1

        if current_page == 1:
            doctor_ids = response.xpath('//*[@class="View_Profile_Button"]//@href').extract()
            last_page = int(response.xpath('//span[@id="FindADoctorResults_Div_Page_Selector__Label_Total"]'
                                           '//text()').extract()[0])
        else:
            data = json.loads(response.body)
            doctor_ids = self.get_doctor_ids(data)
            last_page = data['d']['Number_Of_Pages']

        if last_page == 0:
            yield self.send_next_search_request(response)

        header = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
        index = 0
        size = len(doctor_ids)
        for doctor_id in doctor_ids:
            index += 1
            meta = {}
            if current_page + 1 > last_page and index == size:
                meta = {'search_request': 1}
            elif (last_page != 0 and current_page != last_page) and index == size:
                meta = {'next_page': current_page}
            doc_id = doctor_id.split("'")[1]
            url = base_url + doc_id
            yield Request(url=url, callback=self.parse_profile_contents, headers=header, meta=meta, dont_filter=True)

    def get_doctor_ids(self, data):
        html = data['d']['Html']
        doctor_ids = Selector(text=html).xpath('//*[@class="View_Profile_Button"]//@href').extract()
        return doctor_ids

    def make_pagination_request(self, page):
        url = 'http://www.dignityhealth.org/stmarymedical/FindADoctor/WS_FindADoctor_Results.asmx/Get_Page'
        header = {"Content-Type": "application/json",
                  "X-Requested-With": "XMLHttpRequest",
                  'Accept': 'application/json, text/javascript, */*; q=0.01'}
        payload = json.dumps({"page": str(page)})
        return Request(url, method="POST", body=payload, callback=self.parse_doctor_profiles,
                       headers=header, meta={"page": page}, dont_filter=True)

    def parse_profile_contents(self, response):
        doctor = DoctorProfile()
        doctor['crawled_date'] = str(datetime.datetime.now())
        doctor['gender'] = self.doctor_gender(response)
        doctor['specialty'] = self.doctor_specialty(response)
        doctor['source_url'] = response.url
        doctor['image_url'] = self.doctor_image_url(response)
        doctor['affiliation'] = self.doctor_affiliation(response)
        doctor['medical_school'] = self.doctor_medical_school(response)
        doctor['statement'] = self.doctor_statement(response)
        doctor['full_name'] = self.doctor_full_name(response)
        doctor['address'] = self.doctor_address(response)
        doctor['graduate_education'] = self.doctor_graduate_education(response)

        for key in doctor.keys():
            if not doctor[key]:
                doctor.pop(key)
        yield doctor

        if 'search_request' in response.meta:
            yield self.send_next_search_request(response)

        elif 'next_page' in response.meta:
            yield self.make_pagination_request(response.meta['next_page'] + 1)

    def doctor_gender(self, response):
        gender = response.xpath('//span[contains(@id,"Sex")]//text()').extract()
        if gender:
            return gender[1]

    def doctor_specialty(self, response):
        specialties = []
        specialty = response.xpath('//span[contains(@id,"Specialty")][@class="PersonInfoInfo"]//text()').extract()
        for spec in specialty:
            specialties += [{'name': spec}]
        certification = response.xpath('//div[contains(@id,"Panel_Certifications")]//li//text()').extract()
        for certificate in certification:
            specialties += [{'name': certificate, 'certified': True}]
        return specialties

    def doctor_image_url(self, response):
        return response.xpath('//img[contains(@id,"Image_Person")]//@src').extract()

    def doctor_languages(self, response):
        languages = response.xpath('//span[contains(@id,"Languages")][@class="PersonInfoInfo"]/text()').extract()
        return ' '.join(languages)

    def doctor_affiliation(self, response):
        affiliations = []
        hospitals = response.xpath('//td[@id="Td_Location"]//span[contains(@id,"PracticeLocations_Label_Facility")]'
                                   '/text()').extract()
        for hospital in hospitals:
            affiliation = {'name': hospital}
            if affiliation not in affiliations:
                affiliations += [affiliation]
        return affiliations

    def doctor_medical_school(self, response):
        data = response.xpath('//div[@class="Div_GeneralInformationContent"]//li//text()').extract()
        school = ''
        for org in data:
            if 'Medical School' in org:
                school = org
                break
        if school:
            return school.replace('Medical School - ', '')

    def doctor_statement(self, response):
        statements = response.xpath('//span[@id="FindADoctorProfile_Label_Bio"]/text()').extract()
        if statements:
            for index, statement in enumerate(statements):
                if 'Care' in statement:
                    doc_statement = statements[index] + statements[index + 1] if index < len(statements) - 1 else None
                    return doc_statement.split(':')[-1].strip() if doc_statement else None
        else:
            return None

    def doctor_full_name(self, response):
        return response.xpath('//span[contains(@id,"PersonName")]/text()').extract()[0]

    def doctor_address(self, response):
        addresses = []
        table = response.xpath('//table[@id="Table_PracticeLocations"]//tr')
        for row in table:
            address = {}
            phone = row.xpath('.//span[@class="Label_Phone"]//text()').extract()
            street = row.xpath('.//span[contains(@id,"StreetAddress")]/text()').extract()
            state = row.xpath('.//span[contains(@id,"CityStateZIP")]/text()').extract()
            if street and state:
                address['other'] = [street[0], state[0]]
            if phone:
                address['phone'] = phone[0]
            if address and address not in addresses:
                addresses += [address]
        return addresses

    def doctor_graduate_education(self, response):
        schools = response.xpath('//div[contains(@id,"Education")]//li/text()').extract()
        education = []
        for school in schools:
            school_data = school.split(' - ')
            if len(school_data) == 1:
                education += [{"name": school_data[0]}]
            elif not school_data[0] == 'Medical School':
                education += [{"type": school_data[0], "name": school_data[1]}]
        return education
