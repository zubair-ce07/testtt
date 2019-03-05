import scrapy
from XTO.items import Item
from scrapy.http import Request
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.spiders import CrawlSpider
from w3lib.html import replace_escape_chars
from w3lib.url import url_query_parameter, add_or_replace_parameter


class XTOSpider(CrawlSpider):
    name = 'xto-crawler'

    start_urls = [
        'https://jobs.exxonmobil.com/search/?q=&q2=&alertId=&locationsearch=United+States'
        '&title=&location=US&department=&shifttype=&date=']

    def parse(self, response):

        jobs = response.xpath('//table[@id="searchresults"]')
        for job in jobs.xpath('.//tr'):
            if job.xpath('.//a[@class="jobTitle-link"]//@href').extract():
                yield response.follow(job.xpath('.//a[@class="jobTitle-link"]//@href').extract_first(),
                                      meta={'job_type': self.extract_job_type(job),
                                            'date': self.extract_job_posting_date(job)},
                                      callback=self.parse_job_details)

        current_page = url_query_parameter(response.url, 'startrow') or '0'
        if current_page != self.get_last_page(response):
            next_page_link = add_or_replace_parameter(response.url, 'startrow', int(current_page) + 25)
            yield Request(next_page_link, callback=self.parse)

    def parse_job_details(self, response):

        l = ItemLoader(item=Item(), response=response)
        l.default_input_processor = MapCompose(replace_escape_chars)
        l.default_output_processor = MapCompose(lambda v: v.strip(), replace_escape_chars)
        l.add_xpath('categories', '//span[@itemprop="industry"]//text()')
        l.add_xpath('title', '//span[@itemprop="title"]//text()')
        l.add_xpath('company', '//span[@itemprop="customfield1"]//text()')
        l.add_xpath('logo_urls', '//span[@itemprop="description"]//p//img//@src')
        l.add_xpath('description', '//span[@itemprop="description"]//div//p[4]//text()')
        l.add_xpath('location', '//p[@id="job-location"]//span[@itemprop="jobLocation"]//text()')
        l.add_value('job_types', response.meta['job_type'])
        l.add_value('job_date', response.meta['date'])
        l.add_value('provider', 'exxonmobil')
        l.add_value('external_id', self.extract_external_id(response.url))
        l.add_value('url', response.url)
        return l.load_item()

    def get_last_page(self, response):
        return url_query_parameter(
            response.xpath('//ul[@class="pagination"]//li//a[@class="paginationItemLast"]//@href').extract_first(),
            'startrow')

    def extract_job_type(self, job):
        return job.xpath('.//span[@class="jobShifttype"]//text()').extract()

    def extract_job_posting_date(self, job):
        return job.xpath('.//span[@class="jobDate"]//text()').extract()

    def extract_external_id(self, response):
        return response.split('/')[-2]
