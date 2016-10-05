from scrapy.spiders import Spider
from scrapy.http import Request
from linkedin.items import LinkedinProfilesItem
import csv

class LinkedinProfileSpider(Spider):
    name = 'linkedin_profile_spider'
    allowed_domains = ['www.linkedin.com']
    custom_settings = {'FEED_EXPORTERS': {'json': 'scrapy.exporters.JsonItemExporter',},
                       'FEED_FORMAT': 'json', 'FEED_URI': 'linkedin_profiles_%(time)s.json',
                       'ITEM_PIPELINES': {'linkedin.pipelines.LinkedinProfilesPipeline': 300}
    }

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
                yield Request(url=row['url'], callback=self.parse_linkedin_profile,errback=self.retry_request)

    def parse_linkedin_profile(self, response):
        linkedin_profile = LinkedinProfilesItem()
        linkedin_profile['url'] = response.url
        linkedin_profile['name'] = self.profile_name(response)
        linkedin_profile['location'] = self.profile_location(response)
        linkedin_profile['job_title'] = self.profile_job_title(response)
        linkedin_profile['industry'] = self.profile_industry(response)
        linkedin_profile['extra_info'] = self.profile_extra_info(response)
        linkedin_profile['summary'] = self.profile_summary(response)
        linkedin_profile['experience'] = self.profile_experience(response)
        linkedin_profile['education'] = self.profile_education(response)
        linkedin_profile['languages'] = self.profile_languages(response)
        linkedin_profile['skills'] = self.profile_skills(response)
        linkedin_profile['profile_picture'] = self.profile_picture(response)
        linkedin_profile['certifications'] = self.profile_certifications(response)
        linkedin_profile['publications'] = self.profile_publications(response)
        linkedin_profile['volunteering'] = self.profile_volunteering(response)
        return linkedin_profile

    def profile_name(self, response):
        return response.css('#name::text').extract_first()

    def profile_location(self, response):
        return response.css('.locality::text').extract_first()

    def profile_job_title(self, response):
        return response.css('.headline.title::text').extract_first()

    def profile_industry(self, response):
        return response.css('.descriptor::text').extract_first()

    def profile_extra_info(self, response):
        extra_info_selectors = response.css('.extra-info tr')
        if not extra_info_selectors:
            return
        extra_info = {}
        for extra_info_selector in extra_info_selectors:
            extra_info[''.join(extra_info_selector.xpath('@data-section').extract())] =\
                self.get_text(extra_info_selector.css('td ::text'))
        return extra_info

    def profile_summary(self, response):
        return response.css('.description>p::text').extract()

    def profile_experience(self, response):
        experience = []
        experience_selectors = response.css('#experience li')
        for experience_selector in experience_selectors:
            experience_details = {}
            job_description = ' '.join(experience_selector.css('p ::text').extract())
            if job_description:
                experience_details['job_description'] = job_description
            experience_details['job_title'] = self.get_text(experience_selector.css('h4 ::text'))
            experience_details['company_name'] = self.get_text(experience_selector.css('h5 ::text'))
            experience_details['time_span'] = self.get_text(experience_selector.css('.date-range ::text'))
            experience_details['location'] = self.get_text(experience_selector.css('.location ::text'))
            experience.append(dict((key, value) for key, value in experience_details.items() if value))
        return experience

    def profile_education(self, response):
        education = []
        education_selectors = response.css('#education li')
        for education_selector in education_selectors:
            education_details = {}
            education_details['institute'] = self.get_text(education_selector.css('h4 ::text'))
            education_details['degree'] = self.get_text(education_selector.css('h5 ::text'))
            education_details['time_span'] = self.get_text(education_selector.css('.date-range ::text'))
            education.append(dict((key, value) for key, value in education_details.items() if value))
        return education

    def profile_certifications(self, response):
        certifications = []
        certification_selectors = response.css('#certifications .certification')
        for certification_selector in certification_selectors:
            certification_details = {}
            certification_details['research_type'] = self.get_text(certification_selector.css('h4 ::text'))
            certification_details['institute'] = self.get_text(certification_selector.css('.item-subtitle ::text'))
            certifications.append(dict((key, value) for key, value in certification_details.items() if value))
        return certifications

    def profile_volunteering(self, response):
        return response.css('#volunteering div ::text').extract()

    def profile_publications(self, response):
        publications = []
        publication_selectors = response.css('#publications .publication')
        for publication_selector in publication_selectors:
            publlication_details = {}
            publlication_details['institute'] = self.get_text(publication_selector.css('h4 ::text'))
            publlication_details['publication_titles'] = self.get_text(publication_selector.css('h5 ::text'))
            publlication_details['description'] = self.get_text(publication_selector.css('.description ::text'))
            publlication_details['contributers'] = self.get_text(publication_selector.css('.contributors ::text'))
            publlication_details['date'] = self.get_text(publication_selector.css('.date-range ::text'))
            publications.append(dict((key, value) for key, value in publlication_details.items() if value))
        return publications


    def profile_languages(self, response):
        languages = []
        language_selectors = response.css('#languages li')
        for language_selector in language_selectors:
            language_details = {}
            language_details['name'] = self.get_text(language_selector.css('.name::text'))
            proficiency = self.get_text(language_selector.css('.proficiency::text'))
            if proficiency:
                language_details['proficiency'] = proficiency
            languages.append(language_details)
        return languages

    def profile_skills(self, response):
        return response.css('.skill span::text').extract()

    def profile_picture(self, response):
        return self.get_text(response.css('.profile-picture img::attr(data-delayed-url)'))

    def get_text(self, selector):
        return ' '.join(selector.extract())

    def retry_request(self, failure):
        response = failure.value.response
        if not response.status == 999:
            return
        retries = response.meta.get('retries', 0)
        retries += 1
        if retries > 5:
            args = (5, response.url)
            self.logger.warning('Failed %d times on %s. Giving up.' % args)
        else:
            response.request.meta['retries'] = retries
            response.request.dont_filter = True
            return response.request
