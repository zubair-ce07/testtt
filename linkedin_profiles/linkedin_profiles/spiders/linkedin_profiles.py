from scrapy.spiders import Spider, Rule
from scrapy.http import Request
import csv
from linkedin_profiles.items import LinkedinProfilesItem

class LinkedinProfileSpider(Spider):
    name = 'linkedin_profile_spider'
    allowed_domains = ['www.linkedin.com']

    def __init__(self, *args, **kwargs):
        super(LinkedinProfileSpider, self).__init__(*args, **kwargs)
        filepath = kwargs.get('filepath')
        if not self.filepath:
            raise ValueError('No filepath given')
        self.filepath = filepath

    def start_requests(self):
        return [Request("https://www.linkedin.com", callback=self.parse, meta={'dont_cache': True})]

    def parse(self, response):
        with open(self.filepath) as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield Request(url=row['url'], callback=self.parse_linkedin_profile)

    def parse_linkedin_profile(self, response):
        linkedin_profile = LinkedinProfilesItem()
        linkedin_profile['url'] = response.url
        linkedin_profile['name'] = self.linkedin_profile_name(response)
        linkedin_profile['location'] = self.linkedin_profile_location(response)
        linkedin_profile['job_title'] = self.linkedin_profile_job_title(response)
        industry = self.linkedin_profile_industry(response)
        if industry:
            linkedin_profile['industry'] = industry
        extra_info = self.linkedin_profile_extra_info(response)
        if extra_info:
            linkedin_profile['extra_info'] = extra_info
        summary = self.linkedin_profile_summary(response)
        if summary:
            linkedin_profile['summary'] = summary
        experience = self.linkedin_profile_experience(response)
        if experience:
            linkedin_profile['experience'] = experience
        education = self.linkedin_profile_education(response)
        if education:
            linkedin_profile['education'] = education
        languages = self.linkedin_profile_languages(response)
        if languages:
            linkedin_profile['languages'] = languages
        skills = self.linkedin_profile_skills(response)
        if skills:
            linkedin_profile['skills'] = skills
        profile_picture = self.linkedin_profile_picture(response)
        if profile_picture:
            linkedin_profile['profile_picture'] = profile_picture
        return linkedin_profile

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
                self.clean(extra_info_selector.xpath('.//td//text()'))
        return extra_info

    def linkedin_profile_summary(self, response):
        return response.css('.description>p::text').extract()

    def linkedin_profile_experience(self, response):
        experience = []
        experience_selectors = response.css('#experience li')
        for experience_selector in experience_selectors:
            experience_details = {}
            job_description = ' '.join(experience_selector.xpath('./p//text()').extract())
            if job_description:
                experience_details['job_description'] = job_description
            experience_details['job_title'] = self.clean(experience_selector.xpath('.//h4//text()'))
            experience_details['company_name'] = self.clean(experience_selector.xpath('.//h5//text()'))
            experience_details['further_details'] = self.clean(experience_selector.xpath('.//div//text()'))
            experience.append(experience_details)
        return experience

    def linkedin_profile_education(self, response):
        education = []
        education_selectors = response.css('#education li')
        for education_selector in education_selectors:
            education_details = {}
            education_details['institute'] = self.clean(education_selector.xpath('.//h4//text()'))
            education_details['degree'] = self.clean(education_selector.xpath('.//h5//text()'))
            education_details['time_span'] = self.clean(education_selector.xpath('.//div//text()'))
            education.append(education_details)
        return education

    def linkedin_profile_languages(self, response):
        languages = []
        language_selectors = response.css('#languages li')
        for language_selector in language_selectors:
            language_details = {}
            language_details['name'] = self.clean(language_selector.css('.name::text'))
            language_details['proficiency'] = self.clean(language_selector.css('.proficiency::text'))
            languages.append(language_details)
        return languages

    def linkedin_profile_skills(self, response):
        return response.css('.skill span::text').extract()

    def linkedin_profile_picture(self, response):
        return self.clean(response.css('.profile-picture img::attr(data-delayed-url)'))

    def clean(self, selector):
        return ' '.join(selector.extract())




