import scrapy
import datetime
from scrape.items import ProductLoader, GradstudiesItemLoader, SpecialtyitemLoader, Addressitemloader
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
import itertools


class Doctor(CrawlSpider):

    name = "nwh"
    allowed_domains = ['nwh.org']
    start_urls = [
            'https://www.nwh.org/find-a-doctor/find-a-doctor-home/',
    ]

    rules = [
        Rule(scrapy.linkextractors.LinkExtractor(allow=('r*', ), deny=()), callback='parse_item', follow=True),

        ]

    def parse(self, response):
        return itertools.chain(CrawlSpider.parse(self, response),
            self.parse_item(response))

    def parse_item(self, response):
        if "https://www.nwh.org/find-a-doctor/find-a-doctor-profile" in response.url:
            l = ProductLoader(selector=Selector(response))
            l.add_value('crawled_date', datetime.datetime.now().strftime('%d-%m-%YT%H:%M:%S.%f'))
            l.add_xpath('medical_school', '//*[@id="ctl00_cphContent_ctl01_pnlMedicalSchool"]/ul/li/text()[1]')
            l.add_xpath('fellowship', '//*[@id="ctl00_cphContent_ctl01_pnlFellowship"]/ul/li/text()')
            l.add_xpath('internship', '//*[@id="ctl00_cphContent_ctl01_pnlInternship"]/ul/li/text()')
            l.add_value('source_url', response.url)
            l.add_xpath('board_of_certifications',
                        '//*[@id="ctl00_cphContent_ctl01_pnlBoardOfCertifications"]/ul/li/text()[1]')
            l.add_xpath('image_url',  ' // * [ @class ="col-sm-3"] / div / img / @ src')
            l.add_xpath('full_name', '//*[@id="ctl00_cphContent_ctl01_pnlDocName"]/h1/text()[1]')
            l.add_value('address', self.get_address(response))
            l.add_value('specialty', self.get_specialty(response))
            l.add_value('graduate_studies', self.get_grad(response))
            yield l.load_item()

    def get_address(self, response):
        addressloader = Addressitemloader(selector=Selector(response))
        addressloader.add_xpath('phone', '//*[@id="ctl00_cphContent_ctl01_lblDocContactPhone"]/text()') 
        addressloader.add_xpath('fax', '//*[@id="ctl00_cphContent_ctl01_lblDocContactFax"]/text()')
        addressloader.add_xpath('others',
                                '//*[ @ id = "ctl00_cphContent_ctl01_pnlDocContactLocations"]'
                                '/div/div/div/section/div/a[@ target = "_blank"]//text()')
        yield addressloader.load_item()

    def get_specialty(self, response):
        specialtyloader = SpecialtyitemLoader(selector=Selector(response))
        specialtyloader.add_xpath('name',
                                  'normalize-space(.//*[@id="ctl00_cphContent_ctl01_pnlDocSpecialty"]/h2/text())')
        yield specialtyloader.load_item()

    def get_grad(self, response):
        gradloader = GradstudiesItemLoader(selector=Selector(response))
        gradloader.add_xpath('Type', '//*[@id="ctl00_cphContent_ctl01_pnlResidency"]/h2/text()')
        gradloader.add_xpath('name', '//*[@id="ctl00_cphContent_ctl01_pnlResidency"]/ul/li/text()')
        yield gradloader.load_item()
