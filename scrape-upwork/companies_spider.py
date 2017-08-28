import scrapy
from scrapy import Request
from scrape_upwork.items import CompanyItem
import re
import json

DOWNLOAD_DELAY = 5


class UpworkCompanySpider(scrapy.Spider):
    name = "company_spider"
    allowed_domains = ["upwork.com"]
    start_urls = ['https://www.upwork.com/o/profiles/browse/c/web-mobile-software-dev/?loc=pakistan&q=python']
    headers = {
        'User-agent':
        'Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.7'
    }

    def start_requests(self):
        yield Request(self.start_urls[0], headers=self.headers, callback=self.make_next_pages_request)

    def make_next_pages_request(self, response):
        page_num = 1
        total_pages = 78
        while page_num <= total_pages:
            yield Request(
                self.start_urls[0] + '&page='+str(page_num),
                headers=self.headers, dont_filter=True,
                callback=self.make_user_profile_request)
            page_num += 1

    def make_user_profile_request(self, response):
        users_urls = response.css('div#oContractorResults a::attr(href)').extract()
        companies_urls = []
        for user_url in users_urls:
            companies_urls.extend(re.findall('^/o/companies/.+', user_url))
        companies_urls = list(set(companies_urls))
        print(companies_urls)
        for company_url in companies_urls:
            yield Request('https://www.upwork.com'+company_url, headers=self.headers, callback=self.parse_upwork_item)

    def parse_profile_json(self, response):
        profile_details = response.xpath('//script[contains(.,"var phpVars")]//text()').extract_first()
        profile_details_json = json.loads(str(re.findall('var phpVars\s=\s(\{.*?\});', profile_details)[0]))
        return profile_details_json['agencyProfile']

    def parse_overview(self, profile_info):
        return profile_info['description']

    def parse_name(self, profile_info):
        return profile_info['name']

    def parse_location(self, profile_info):
        return {'city': profile_info['city'], 'country': profile_info['country']}

    def parse_assignments_info(self, profile_info):
        totalassignments = profile_info['assignmentsEnded']['assignments']
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

    def parse_profile_title(self, profile_info):
        return profile_info['title']

    def parse_work_history(self, profile_info):
        return {'member_since': profile_info['memberSince'], 'jobSuccessScore': profile_info['jobSuccessScore'],
                'totalJobsWorked': profile_info['totalJobs'], 'totalHours': profile_info['totalHours']}

    def parse_managers_info(self, profile_info):
        managers = profile_info['managers']
        managers_details = []
        for manager in managers:
            managers_details.append({
                'identity': manager['ciphertext'],
                'name': manager['name'],
                'isagencyOwner': manager['agencyOwner']})
        return managers_details

    def parse_website(self, profile_info):
        return profile_info['company']['website']

    def parse_upwork_item(self, response):
        profile_info = self.parse_profile_json(response)
        company_item = CompanyItem()
        company_item['overview'] = self.parse_overview(profile_info)
        company_item['name'] = self.parse_name(profile_info)
        company_item['location'] = self.parse_location(profile_info)
        company_item['assignments'] = self.parse_assignments_info(profile_info)
        company_item['url'] = response.url
        company_item['managers'] = self.parse_managers_info(profile_info)
        company_item['title'] = self.parse_profile_title(profile_info)
        company_item['workHistory'] = self.parse_work_history(profile_info)
        company_item['website'] = self.parse_website(profile_info)
        return company_item
