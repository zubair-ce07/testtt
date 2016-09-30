from scrapy.spiders import Spider, Rule
from scrapy.http import Request
import csv
from linkedin_profiles.items import LinkedinProfilesItem
from scrapy.linkextractors import LinkExtractor
import re

class LinkedinProfileSpider(Spider):
    name = 'linkedin_profile_spider'
    allowed_domains = ['www.linkedin.com']

    def start_requests(self):
        return [Request("https://www.linkedin.com", callback=self.parse, meta={'dont_cache': True})]

    def parse(self, response):
        with open('output.csv') as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield Request(url=row['url'],
                       callback=self.parse_linkedin_profile)

    def parse_linkedin_profile(self, response):
        linkedin_profile = LinkedinProfilesItem()
        linkedin_profile['name'] = self.linkedin_profile_name(response)
        linkedin_profile['location'] = self.linkedin_profile_location(response)
        linkedin_profile['job_title'] = self.linkedin_profile_job_title(response)
        industry = self.linkedin_profile_industry(response)
        if industry:
            linkedin_profile['industry'] = industry
        extra_info = self.linkedin_profile_extra_info(response)
        if extra_info:
            linkedin_profile['extra_info'] = extra_info
        pass

    def linkedin_profile_name(self, response):
        return ' '.join(response.css('#name::text').extract())

    def linkedin_profile_location(self, response):
        return ' '.join(response.css('.locality::text').extract())

    def linkedin_profile_job_title(self, response):
        return ' '.join(response.css('.headline.title::text').extract())

    def linkedin_profile_industry(self, response):
        return ' '.join(response.css('.descriptor::text').extract())

    def linkedin_profile_extra_info(self, response):
        extra_info_selectors = response.css('.extra-info tr')
        if not extra_info_selectors:
            return ''
        extra_info = {}
        for extra_info_selector in extra_info_selectors:
            extra_info[''.join(extra_info_selector.xpath('@data-section').extract())] =\
                ''.join(extra_info_selector.xpath('//td//text()').extract())
        return extra_info
