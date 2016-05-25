import datetime
import json
import scrapy
import string
from scrapy.http import FormRequest, Request
from mhealth.items import DoctorProfile


class MHealthSpider(scrapy.Spider):
    name = "mhealth_spider"
    allowed_domains = ["mhealth.org"]
    start_urls = [
        'https://www.mhealth.org/providers'
    ]
    first_result = 0
    search_params = list(string.lowercase)
    search_key = ''

    def parse(self, response):
        if self.search_params and self.first_result == 0:
            self.search_key = self.search_params.pop(0)
        url = 'https://www.mhealth.org/coveo/rest/?errorsAsSuccess=1'
        return FormRequest(url=url,
                           formdata={
                               'aq': '(@fisz32xproviderz32xbio41631=1 AND '
                                     '@fhidez32xfromz32xallz32xsitez32xsearches41631=0 AND '
                                     '@fhidez32xfromz32xmz32xhealthz32xsitez32xsearch41631=0) '
                                     '(@fproviderz32xlastz32xinitial41631=={})'.format(self.search_key),
                               'firstResult': str(self.first_result)},
                           callback=self.parse_list)

    def parse_list(self, response):
        data = json.loads(response.body)
        for doctor in data['results']:
            url = doctor['clickUri']
            yield Request(url=url, callback=self.parse_doctor_profile)
        self.first_result += 10
        if self.first_result > data['totalCount']:
            self.first_result = 0
        if not (self.first_result == 0 and not self.search_params):
            yield self.parse(response)

    def parse_doctor_profile(self, response):
        doctor = DoctorProfile()
        doctor['crawled_date'] = str(datetime.datetime.now())
        doctor['affiliation'] = self.doctor_affiliation(response)
        doctor['specialty'] = self.doctor_specialty(response)
        doctor['source_url'] = response.url
        doctor['languages'] = self.doctor_languages(response)
        doctor['image_url'] = self.doctor_image_url(response)
        doctor['clinical_interest'] = self.doctor_clinical_interest(response)
        doctor['medical_school'] = self.doctor_medical_school(response)
        doctor['full_name'] = self.doctor_full_name(response)
        doctor['address'] = self.doctor_address(response)
        doctor['graduate_education'] = self.doctor_graduate_education(response)

        for key in doctor.keys():
            if not doctor[key]:
                doctor.pop(key)
        yield doctor

    def doctor_specialty(self, response):
        specialty = []
        specialties = response.xpath('//div[contains(@class,"specialties-and-services")]//a/text()').extract()
        for skill in specialties:
            specialty += [{"name": skill}]
        certifications = response.xpath('//div[@class="education"]//div[contains(text(),"Certifications")]'
                                        '/following-sibling::div//text()').extract()
        certifications = filter(None, [certificate.strip() for certificate in certifications])
        for certificate in certifications:
            specialty += [{"name": certificate, "certified": True}]
        return specialty

    def doctor_image_url(self, response):
        image_url = response.xpath('//div[contains(@class,"introduction")]//img/@src').extract()
        return 'https://www.mhealth.org' + image_url[0] if image_url else None

    def doctor_affiliation(self, response):
        affiliations = []
        affiliation = response.xpath('//div[contains(@class,"titles")]/text()').extract()[0].strip()
        if affiliation:
            affiliations += [{"title": affiliation}]
        if response.xpath('//div[@class="clinic"]'):
            affiliations += [{"name": response.xpath('//div[@class="clinic"]/div/text()').extract()[0].strip()}]
        academic_affiliation = response.xpath(
            '//div[@class="academic-information content-block"]//p[@class="title line"]//text()').extract()
        if academic_affiliation:
            affiliations += [{"title": academic_affiliation[0].strip()}]
        return affiliations

    def doctor_medical_school(self, response):
        schools = response.xpath('//div[@class="education"]//div[contains(text(),"Medical School")]'
                                 '/following-sibling::div//text()').extract()
        schools = filter(None, [school.strip() for school in schools])
        med_school = []
        for school in schools:
            med_school += [{"name": school}]
        return med_school

    def doctor_languages(self, response):
        languages = response.xpath('//div[contains(@class,"languages")]//div//text()').extract()
        return languages[1].strip() if languages else None

    def doctor_clinical_interest(self, response):
        interests = response.xpath('//div[@class="care-and-clinical-interests"]//div[contains(text(),'
                                   '"Clinical Interests")]/following-sibling::ul//li//text()').extract()
        interests = filter(None, [index.strip() for index in interests])
        return interests

    def doctor_full_name(self, response):
        return response.xpath('//h2//text()').extract()[0]

    def doctor_address(self, response):
        address_bar = response.xpath('//div[@class="clinic"]')
        addresses = []
        for address in address_bar:
            location = address.xpath('.//div[@class="body-text"]/text()').extract()
            location.insert(0, address.xpath('./a/text()').extract()[0])
            location = [index.strip() for index in location]
            addresses += [{"other": location}]
        return addresses

    def doctor_graduate_education(self, response):
        grad_education = []
        residency = response.xpath(
            '//div[@class="education"]//div[contains(text(),"Residency")]/following-sibling::div//text()').extract()
        residency = filter(None, [school.strip() for school in residency])
        for school in residency:
            grad_education += [{"type": "Residency", "name": school}]
        fellowship = response.xpath(
            '//div[@class="education"]//div[contains(text(),"Fellowship")]/following-sibling::div//text()').extract()
        fellowship = filter(None, [school.strip() for school in fellowship])
        for school in fellowship:
            grad_education += [{"type": "Fellowship", "name": school}]
        other_education = response.xpath(
            '//div[@class="education"]//div[contains(text(),"Other")]/following-sibling::div//text()').extract()
        other_education = filter(None, [school.strip() for school in other_education])
        for school in other_education:
            grad_education += [{"type": "Other Education", "name": school}]
        return grad_education
