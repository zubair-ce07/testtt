"""
Spider to Scrape details of doctors from
Newton Wellesley Hospital's site
"""
# -*- coding: utf-8 -*-
from datetime import datetime
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
import NWHScrapper.utilities as util
from NWHScrapper.items import NwhDoctor


class NWHSpider(scrapy.Spider):
    """
    Spider class to scrape doctor details.
    """
    name = 'nwhspider'
    allowed_domains = ['www.nwh.org']
    start_urls = ['https://www.nwh.org/find-a-doctor/find-a-doctor-home']

    def parse(self, _):
        """
        Do a POST request to get links of all doctors' profiles
        :param _: response from hitting start_url
        :return: Yield POST request to get list of profiles
        """
        # create request to get all doctors
        request_data = util.prepare_search_request()
        yield scrapy.FormRequest(
            url=request_data['url'],
            method='POST',
            formdata=request_data['data'],
            callback=self.parse_doctors
        )

    def parse_profile(self, response):
        """
        Use Item Loaders to parse profile details
        from given response
        :param response: response from hitting profile url
        :return: NwhScrapperItem object containing
        scraped details of doctor.
        """
        doctor_loader = ItemLoader(item=NwhDoctor(),
                                   response=response)
        doctor_loader.default_output_processor = TakeFirst()

        doctor_loader.add_value('source_url',
                                response.url)
        doctor_loader.add_value('crawled_date',
                                str(datetime.now()))
        doctor_loader.add_value('full_name',
                                util.parse_name(response))
        doctor_loader.add_value('address',
                                util.parse_address(response))
        doctor_loader.add_value('image_url',
                                util.parse_image_url(response))
        doctor_loader.add_value('speciality',
                                util.parse_speciality(response))
        doctor_loader.add_value('affiliation',
                                util.parse_affiliation(response))
        doctor_loader.add_value('graduate_education',
                                util.parse_education(response))
        doctor_loader.add_value('medical_school',
                                util.parse_medical_school(response))

        yield doctor_loader.load_item()

    def parse_doctors(self, response):
        """
        Parse profile urls from response and
         yield request to parse each profile
        :param response: response of POST request
         done be self.parse()
        :return: yield GET requests for all profiles
        """
        # retrieve list of all profile links
        profile_urls = util.make_profile_urls(response)
        # yield requests to parse each profile
        for profile_url in profile_urls:
            yield scrapy.Request(profile_url,
                                 callback=self.parse_profile,
                                 dont_filter=True,)
