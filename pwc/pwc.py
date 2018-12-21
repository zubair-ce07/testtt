import scrapy
from pwc.items import Item
from scrapy.http import Request
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider


class PWCSpider(CrawlSpider):
    name = 'pwc-crawler'

    start_urls = ['https://jobs.pwc.com/ListJobs/All/', 'https://campusjobs.pwc.com/ListJobs/All']

    def parse(self, response):
        jobs = response.xpath('//table[@class="JobListTable"]')

        for job in jobs.xpath('.//tr'):
            if job.xpath('.//td[@class="coloriginaljobtitle"]//a//@href').extract():
                yield response.follow(job.xpath('.//td[@class="coloriginaljobtitle"]//a//@href').extract_first(),
                                      callback=self.parse_job_details)

        if response.xpath('//a[@class="pager-next-arrow"]').extract():
            yield response.follow('Page-{}'.format(
                int(response.xpath('//span[@class="current"]//text()').extract_first()) + 1), callback=self.parse)

    def parse_job_details(self, response):

        l = ItemLoader(item=Item(), response=response)
        l.add_xpath('categories', '//div[@class="col1"]//div[1]//span//text()')
        l.add_xpath('title', '//h1[@class="detailHeading"]//text()')
        l.add_xpath('description', '//div[@class="description"]//text()')
        l.add_xpath('job_types', '//div[@class="col1"]//div[6]//span//text()')
        l.add_xpath('location', '//div[@class="col2"]//div[1]//span//text()')
        l.add_xpath('external_id', '//div[@class="col2"]//div[5]//span//text()')
        l.add_value('provider', 'pwc US careers')
        l.add_value('url', response.url)
        return l.load_item()
