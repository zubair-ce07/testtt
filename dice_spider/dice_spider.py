import scrapy
from items import JobLoader
from scrapy.http import FormRequest
from urlparse import urljoin


class DiceSpider(scrapy.Spider):
    name = "dice_spider"
    start_urls = [
        'https://www.dice.com/'
    ]

    def next_page(self, response):
        response.follow(response.xpath('//link[@rel="next"]/@href')
                              .extract_first(), self.parse)

    def parse(self, response):
        states_to_scrape = ['New York', 'Connecticut']
        for state in states_to_scrape:
            yield FormRequest.from_response(
                response,
                formxpath='//input[@placeholder="Location"]',
                formdata={'l':state},
                callback=self.search_results
            )

    def parse_job(self, response):
        job = JobLoader(selector=response)
        job.add_xpath('categories','//div[@itemprop="skills"]/text()')
        job.add_xpath('company', '//span[@itemprop="name"]/text()')
        job.add_xpath('company_url', '//li[@class="employer"]/a/@href')
        job.add_xpath('description', '//div[@id="jobdescSec"]//text()')
        job.add_xpath('external_id', '//meta[@name="jobId"]/@content')
        job.add_xpath('job_date', '//li[@class="posted hidden-xs"]/text()')
        job.add_xpath('job_types', '//meta[@itemprop="employmentType"]/'
                                   'preceding-sibling::span/text()')
        job.add_xpath('location', '//input[@id="location"]/@value')
        job.add_xpath('logo_urls', '//img[@class="h-logo"]/@src')
        job.add_value('provider', 'dice')
        job.add_xpath('salary', '//span[@itemprop="baseSalary"]'
                                '/preceding-sibling::span/text()')
        job.add_xpath('title', '//h1/text()')
        job.add_xpath('url', '//link[@rel="canonical"]/@href')
        return job.load_item()

    def search_results(self, response):
        for href in response.xpath('//*[@id="search-results-control"]'
                                   '//div[contains(@class,"serp-result")]'
                                   '/ul[@class="list-inline"]//a/@href') \
                .extract():
            yield scrapy.Request(urljoin('https://www.dice.com',href)
                                 , self.parse_job)

        yield self.next_page(response)
