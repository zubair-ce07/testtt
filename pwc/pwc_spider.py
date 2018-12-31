import scrapy
from pwc.items import Item
from scrapy.http import Request
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider


class PWCSpider(CrawlSpider):
    name = 'pwc-crawler'

    start_urls = ['https://jobs.pwc.com/ListJobs/All/', 'https://campusjobs.pwc.com/ListJobs/All']

    def parse(self, response):
        jobs = response.xpath('//table[@class="JobListTable"]//tr')

        for job in jobs:
            if job.xpath('.//td[@class="coloriginaljobtitle"]//a//@href').extract():
                yield response.follow(job.xpath('.//td[@class="coloriginaljobtitle"]//a//@href').extract_first(),
                                      callback=self.parse_job_details)

        if self.extract_next_pager_button(response):
            yield self.make_pagination_request(response)

    def make_pagination_request(self, response):
        return response.follow('Page-{}'.format(int(self.extract_current_page(response)) + 1), callback=self.parse)

    def parse_job_details(self, response):

        item_loader = ItemLoader(item=Item(), response=response)
        item_loader.add_xpath('categories', '//div[@class="col1"]//div[1]//span//text()')
        item_loader.add_xpath('title', '//h1[@class="detailHeading"]//text()')
        item_loader.add_xpath('description', '//div[@class="description"]//text()')
        item_loader.add_xpath('job_types', '//div[@class="col1"]//div[7]//span//text()')
        item_loader.add_value('logo_urls', 'https://pbs.twimg.com/profile_images/1017853710054158336/_E8Vz_Id_400x400.jpg')
        item_loader.add_value('provider', 'pwc_corporate')
        item_loader.add_value('url', response.url)

        if len(self.extract_job_location(response)) > 1:
            for location in self.extract_job_location(response):
                item_loader.replace_value('location', self.modify_location_format(location))
                item_loader.replace_value('external_id', '{}_{}'.format(self.extract_external_id(response),
                                                                        self.modify_location_format(location)))
                yield item_loader.load_item()

        else:
            item_loader.add_value('location', self.modify_location_format(self.extract_job_location(response)[0]))
            item_loader.add_value('external_id', self.extract_external_id(response))
            yield item_loader.load_item()

    def extract_job_location(self, response):
        location = response.xpath('//div[@class="col2"]//div[1]//span//text()').extract()
        loc = location[0].split('|')
        return loc

    def extract_external_id(self, response):
        return response.xpath('//div[@class="col2"]//div[5]//span//text()').extract_first()

    def modify_location_format(self, location):
        return '{}-{}'.format(location.split('-')[1], location.split('-')[0])

    def extract_next_pager_button(self, response):
        return response.xpath('//a[@class="pager-next-arrow"]').extract()

    def extract_current_page(self, response):
        return response.xpath('//span[@class="current"]//text()').extract_first()
