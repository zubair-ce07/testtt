from items import JobLoader
from scrapy.http import FormRequest
import scrapy


def concatenate_urls(a, b):
    if b == None:
        return None
    else:
        return '{}{}'.format(a, b)


def process_str(response, xpath):
    result = response.xpath(xpath).extract_first()
    if result == None:
        return None
    else:
        return result.strip().replace(' ', '').split(",")


class DiceSpider(scrapy.Spider):
    name = "dice_spider"
    start_urls = [
        'https://www.dice.com/'
    ]

    def next_page(self, response):
        response.follow(response.xpath("//link[@rel='next']/@href")
                              .extract_first(), self.parse)

    def parse(self, response):
        return [FormRequest.from_response(
            response,
            formxpath='//input[@placeholder="Location"]',
            formdata={
                'l':'New York'
            },
            callback=self.search_results
        ), FormRequest.from_response(
            response,
            formxpath='//input[@placeholder="Location"]',
            formdata={
                'l':'Connecticut'
            },
            callback=self.search_results
        )]

    def parse_job(self, response):
        job = JobLoader(selector=response)
        categories = process_str(response, '//div[@itemprop="skills"]/text()')
        job.add_value('categories',categories)
        job.add_xpath('company', '//span[@itemprop="name"]/text()')
        company_url = concatenate_urls("https://www.dice.com", response
                                       .xpath('//li[@class="employer"]/a'
                                              '/@href').extract_first())
        job.add_value('company_url', company_url)
        job.add_xpath('description', '//div[@id="jobdescSec"]//text()')
        job.add_xpath('external_id', '//meta[@name="jobId"]/@content')
        job.add_xpath('job_date', '//li[@class="posted hidden-xs"]/text()')
        job_types = process_str(response, '//meta[@itemprop="employmentType"]'
                                          '/preceding-sibling::span/text()')
        job.add_value('job_types', job_types)
        job.add_xpath('location', '//input[@id="location"]/@value')
        logo_url = concatenate_urls("https:", (response.xpath('//img[@class='
                                                              '"h-logo"]/@src')
                                               .extract_first()))
        job.add_value('logo_urls', logo_url)
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
            yield response.follow(href, self.parse_job)

        yield self.next_page(response)
