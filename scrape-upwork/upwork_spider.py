import scrapy
from scrapy import Request
from scrape_upwork.items import ProfileItem
import re
import json

DOWNLOAD_DELAY = 5


class UpworkSpider(scrapy.Spider):
    name = "upwork_spider"
    allowed_domains = ["upwork.com"]
    start_urls = ['https://www.upwork.com/o/profiles/browse/c/web-mobile-software-dev/?loc=pakistan&q=python']
    headers = {
        'User-agent':
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'
    }

    def start_requests(self):
        yield Request(self.start_urls[0], headers=self.headers, callback=self.make_next_pages_request)

    def make_next_pages_request(self, response):
        page_num = 1
        total_pages = 5
        while page_num <= total_pages:
            yield Request(
                self.start_urls[0] + '&page='+str(page_num),
                headers=self.headers, dont_filter=True,
                callback=self.make_user_profile_request)
            page_num += 1

    def make_user_profile_request(self, response):
        users_urls = response.css('div#oContractorResults a::attr(href)').extract()
        profile_urls = []
        for user_url in users_urls:
            profile_urls.extend(re.findall('^/o/profiles/users/.+', user_url))
        profile_urls = list(set(profile_urls))
        for profile_url in profile_urls:
            yield Request('https://www.upwork.com'+profile_url, headers=self.headers, callback=self.parse_upwork_item)

    def parse_profile_json(self, response):
        profile_details = response.xpath('//script[contains(.,"var phpVars")]//text()').extract_first()
        profile_details_json = json.loads(str(re.findall('var phpVars\s=\s(\{.*?\}\});', profile_details)[0]))
        return profile_details_json['profileSettings']['profile']

    def parse_employment_history(self, profile_info):
        return profile_info['employmentHistory']

    def parse_overview(self, profile_info):
        return profile_info['profile']['description']

    def parse_name(self, profile_info):
        return profile_info['profile']['name']

    def parse_location(self, profile_info):
        location = profile_info['profile']['location']
        return {'city': location['city'], 'country': location['country']}

    def parse_skills(self, profile_info):
        skills = profile_info['profile']['skills']
        skills_name = []
        for skill in skills:
            skills_name.append(skill['name'])
        return skills_name

    def parse_education_info(self, profile_info):
        return profile_info['education']

    def parse_portfolios(self, profile_info):
        return profile_info['portfolios']

    def parse_test_info(self, profile_info):
        tests = profile_info['tests']
        tests_info = []
        for test in tests:
            if test:
                tests_info.append({'name': test['name'], 'provider': test['provider'],
                                   'isPassed': test['isPassed'], 'score': test['score']})
        return tests_info

    def parse_assignments_info(self, profile_info):
        totalassignments = profile_info['assignments']
        totalassignments.extend(profile_info['assignmentsInProgress'])
        assignments_details = []
        feedback = {}
        for assignment in totalassignments:
            feedback_element = assignment['feedback']
            if feedback_element:
                feedback = {'comment': feedback_element['comment'], 'score': feedback_element['score']}
            title = assignment['title']
            description = assignment['description']
            startedOn = assignment['startedOn']
            endedOn = assignment['endedOn']
            if not endedOn:
                endedOn = 'Present'
            assignments_details.append({
                'title': title,
                'description': description,
                'feedback': feedback,
                'startedOn': startedOn,
                'endedOn': endedOn})
        return assignments_details

    def parse_identity_info(self, profile_info):
        return profile_info['identity']['ciphertext']

    def parse_profile_title(self, profile_info):
        return profile_info['profile']['title']

    def parse_work_history(self, profile_info):
        stats = profile_info['stats']
        return {'member_since': stats['memberSince'], 'rating': stats['rating'],
                'totalJobsWorked': stats['totalJobsWorked'], 'totalHours': stats['totalHours']}

    def parse_upwork_item(self, response):
        profile_info = self.parse_profile_json(response)
        profile_item = ProfileItem()
        profile_item['employmentHistory'] = self.parse_employment_history(profile_info)
        profile_item['overview'] = self.parse_overview(profile_info)
        profile_item['name'] = self.parse_name(profile_info)
        profile_item['location'] = self.parse_location(profile_info)
        profile_item['skills'] = self.parse_skills(profile_info)
        profile_item['education'] = self.parse_education_info(profile_info)
        profile_item['portfolios'] = self.parse_portfolios(profile_info)
        profile_item['tests'] = self.parse_test_info(profile_info)
        profile_item['assignments'] = self.parse_assignments_info(profile_info)
        profile_item['url'] = response.url
        profile_item['identity'] = self.parse_identity_info(profile_info)
        profile_item['title'] = self.parse_profile_title(profile_info)
        profile_item['workHistory'] = self.parse_work_history(profile_info)
        return profile_item



