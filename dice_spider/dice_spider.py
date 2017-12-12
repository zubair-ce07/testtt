from scrapy.loader import ItemLoader
from scrapy.loader.processors import Compose, Join, TakeFirst
from items import Job
import scrapy


class DiceSpider(scrapy.Spider):
    name = "jobs"
    start_urls = [
        'https://www.dice.com/jobs/sort-date-l-New_York%2C_NY-radius-30-'
        'startPage-1-jobs?searchid=8688587652890&stst=',
        'https://www.dice.com/jobs/sort-date-l-Connecticut-radius-30-'
        'startPage-1-jobs?searchid=8700101275628&stst=',
    ]

    def parse(self, response):
        for href in response.xpath("//div[@id='search-results-control']/div"
                                   "/div/div/div/ul/li/h3/a/@href").extract():
            yield response.follow(href, self.parse_job)

        yield response.follow(response.xpath("//link[@rel='next']/@href")
                              .extract_first(), self.parse)

    def parse_job(self, response):
        try:
            job = ItemLoader(item=Job(), response=response)
            job.default_output_processor = TakeFirst()
            categories = response.xpath('//div[@itemprop="skills"]/text()')\
                .extract_first().replace('\n', '').replace('\t', '')\
                .replace(' ', '').split(",")
            job.categories_out = Compose()
            job.add_value('categories',categories)
            job.add_xpath('company', '//span[@itemprop="name"]/text()')
            company_url = "https://www.dice.com"+response\
                .xpath('//a[@id="companyNameLink"]/@href').extract_first()
            job.add_value('company_url', company_url)
            job.description_out = Join()
            job.add_xpath('description', '//div[@id="jobdescSec"]//text()')
            job.add_xpath('external_id', '//meta[@name="jobId"]/@content')
            job.add_xpath('job_date', '//li[@class="posted hidden-xs"]/text()')
            job_types = response.xpath('//meta[@itemprop="employmentType"]/'
                                       'preceding-sibling::span/text()')\
                .extract_first().replace(" ", "").split(",")
            job.job_types_out = Compose()
            job.add_value('job_types', job_types)
            job.add_xpath('location', '//input[@id="location"]/@value')
            logo_url = ["https:" + s for s in (response
                                               .xpath('//img[@class="h-logo"]'
                                                      '/@src').extract())]
            job.logo_urls_out = Compose()
            job.add_value('logo_urls', logo_url)
            job.add_value('provider', 'dice')
            job.add_xpath('salary', '//span[@itemprop="baseSalary"]'
                                    '/preceding-sibling::span/text()')
            job.add_xpath('title', '//h1/text()')
            job.add_xpath('url', '//link[@rel="canonical"]/@href')
            return job.load_item()
        except:
            pass
