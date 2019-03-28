# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from ..items import JobItem


class IndeedSpider(CrawlSpider):
    name = 'indeed-us'
    allowed_domains = ['indeed.com']
    start_urls = ['https://www.indeed.com/find-jobs.jsp?from=HP2']
    custom_settings = {
        'DOWNLOAD_DELAY': 5.0,
        'COOKIES_ENABLED': False
    }

    jobs_css = ['.job']
    listings_css = ['#categories']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=jobs_css), callback='parse_item')
    )

    filter_map = {
        '#SALARY_rbo li': 'Salary Estimate',
        '#JOB_TYPE_rbo li': 'Job Type',
        '#LOCATION_rbo li': 'Location',
        '#COMPANY_rbo li': 'Company',
        '#EXP_LVL_rbo li': 'Experience Level'
    }

    def parse(self, response):
        for request in list(super().parse(response)):
            request.meta['category'] = response.meta.get('link_text', '')
            yield request

    def parse_item(self, response):
        title = response.css('[id="what"]::attr(value)').extract_first()
        for job_css, heading in self.filter_map.items():
            if not response.css(job_css):
                continue

            for job_s in response.css(job_css):
                job = JobItem()
                job['title'] = response.meta.get("category", "") + '|' + title
                job['type'] = heading
                job['attribute'] = job_s.css('a::text').extract_first()
                job['job_count'] = job_s.css('li::text').re_first(r'\((.*)\)')
                yield job
