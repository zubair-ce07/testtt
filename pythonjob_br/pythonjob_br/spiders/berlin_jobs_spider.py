import re

from scrapy.spiders import CrawlSpider, Rule, Request
from scrapy.linkextractors import LinkExtractor

from ..items import BerlinJobItem


class BerlinJobsSpider(CrawlSpider):
    name = 'berlinjobs'
    start_urls = ['https://stackoverflow.com/jobs?sort=i&q=pyhton&l=Berlin%2C+Germany&d=20&u=Km']
    visited_items = set()
    rules = (
        Rule(LinkExtractor(restrict_css='.test-pagination-next')),
        Rule(LinkExtractor(restrict_css='.-row .-title .job-link'), callback='parse_item'),
    )

    def parse_item(self, response):
        p_id = "".join(re.findall('jobs\/(\d+)\/', response.url))
        if self.is_visited(p_id):
            return
        item = BerlinJobItem()
        item['title'] = self.title(response)
        item['company'] = self.company(response)
        item['location'] = self.location(response)
        item['perks'] = self.perks(response)
        item['technologies'] = self.technologies(response)
        item['description'] = self.description(response)
        yield item

    def title(self, response):
        return response.css('.job-detail-header .-title a::text').extract_first()

    def company(self, response):
        return response.css('.job-detail-header .-company .employer::text').extract_first()

    def location(self, response):
        return self.clean(response.css('.job-detail-header .-company .-location::text').extract_first())

    def perks(self, response):
        return self.clean(response.css('.job-detail-header .-perks p::text').extract())

    def technologies(self, response):
        return response.css('.-technologies .-tags a::text').extract()

    def description(self, response):
        job_d = {}
        des_sel = response.css('.-about-job-items .-item')
        for s in des_sel:
            key = self.clean(s.css('.-key::text').extract_first())
            job_d[key] = s.css('.-value::text').extract_first()
        return job_d

    def clean(self, to_clean):
        if isinstance(to_clean, str):
            return re.sub('\s+', ' ', to_clean).strip()
        return [re.sub('\s+', ' ', d).strip() for d in to_clean if d.strip()]

    def is_visited(self, item_id):
        if item_id in self.visited_items:
            return True
        self.visited_items.add(item_id)
        return False
