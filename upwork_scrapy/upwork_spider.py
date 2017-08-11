import scrapy
import datetime
from upwork_scrapy.items import UpworkScrapyItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose


headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/60.0.3112.78 Safari/537.36'}


class Upwork(scrapy.Spider):

    name = "up_work_spider"
    allowed_domains = ['upwork.com']
    start_urls = ['https://www.upwork.com/o/jobs/browse/c/sales-marketing/']
    
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, headers=headers, errback=self.error_http, callback=self.parse)

    def error_http(self, failure):
        self.logger.error(repr(failure))

    def parse(self, response):
        get_job_pages = scrapy.Selector(response)
        next_page_links = get_job_pages.xpath('//*[@id="jobs-list"]/section[11]/div/ul/li[7]/a/@href').extract()
        all_links = get_job_pages.xpath('//div[1]/div/header/h2/a/@href').extract()
        for pages in next_page_links:
            up_url = 'https://www.upwork.com'
            for link in all_links:
                full_link = up_url + str(link)
                yield scrapy.http.Request(url=full_link, headers=headers, errback=self.error_http,
                                          callback=self.parse_job_profile)
                page_url = up_url + str(pages)
                yield scrapy.http.Request(url=page_url, headers=headers, errback=self.error_http, callback=self.parse)

    def parse_job_profile(self, response):
        up_work = ItemLoader(UpworkScrapyItem(), response)
        up_work.add_value('crawled_at', datetime.datetime.now().strftime('%d-%m-%YT%H:%M:%S'))
        up_work.add_xpath('categories', '//div[2]/div/a[contains(@class, tag-skill)]/text()',
                          MapCompose(lambda v: v.strip('\n  ').split('-')))
        up_work.add_xpath('description', 'normalize-space(//*[@id="layout"]//div[2]/div[1]/p[contains(@class, break)])')
        up_work.add_xpath('experience', '//div[2]/div/p[@class="m-0-bottom"]/strong/text()',
                          MapCompose(lambda v: v.split(' ')), TakeFirst())
        up_work.add_value('url', response.url)
        up_work.add_xpath('job_types', '//div[1]/div[1]/div/p[@class="m-0-bottom"]/strong/text()',
                          MapCompose(lambda v: v.split(' ')), TakeFirst())
        up_work.add_value('provider',  'upwork')
        up_work.add_xpath('title', '//h1[@class="m-0-top"]/text()')
        up_work.add_value('external_id', response.url,  MapCompose(lambda v: v.strip('/').partition('_')[2:]))
        up_work.add_xpath('project_type', '//*[@id="form"]/li[2]/text()', MapCompose(lambda v: v.strip('\n  ')))
        up_work.add_xpath('client_rating', '//*[@itemprop="ratingValue"]/text()')
        up_work.add_xpath('client_reviews', '//*[@itemprop="ratingCount"]/text()')
        up_work.add_xpath('job_posted_location', 'normalize-space(//div[2]/p[2]/span[@class="text-muted"]/text())',
                          MapCompose(lambda v: v.rstrip('PAM123456789:0 ')))
        up_work.add_xpath('jobs_posted', 'normalize-space(//p[3]/strong/text())',
                          MapCompose(lambda v: v.split(' ')), TakeFirst())
        up_work.add_xpath('hire_rate', 'normalize-space(//div[2]/p[3]/span/text())',
                          MapCompose(lambda v: v.split(' ')), TakeFirst())
        up_work.add_xpath('budget', '//div[1]/div[2]/small[@class="text-muted"]/text()',
                          MapCompose(lambda v: v.partition('$')[2:]))
        up_work.add_xpath('other_skills', '//*[@ng-repeat="skill in skills"]/a[contains(@ng-if,"skill.prettyName")]')

        yield up_work.load_item()
