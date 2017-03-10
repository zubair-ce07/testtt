import scrapy
from scrapy.loader import ItemLoader
from ..items import Job
from datetime import datetime
import re


class DiceSpider(scrapy.Spider):
    name = "dice_test"

    start_urls = [
        'https://www.dice.com/jobs?l=NY&startPage=1',
        'https://www.dice.com/jobs?l=CT&startPage=1'
    ]

    def parse(self, response):
        if not response:
            return

        # follow links to author pages
        for href in response.xpath('//div[@id="search-results-control"]//a[contains(@id, "position")]/@href').extract():
            print("HREF::")
            print(href)
            yield scrapy.Request(href, callback=self.parse_job_details)

        # for href in response.css('.author + a::attr(href)'):
        #     yield response.follow(href, self.parse_job_details)
        #
        # next_page = response.css('li.next a::attr("href")').extract_first()
        # if next_page is not None:
        #     yield response.follow(next_page, self.parse)
        #
        # # follow pagination links
        # for href in response.css('li.next a::attr(href)'):
        #     yield response.follow(href, self.parse)

        "https://www.dice.com/jobs/sort-date-limit-30-l-NY-radius-30-startPage-1-limit-30-jobs"
        startPage_match = re.search("startPage=(\d+)", response.url)
        if startPage_match:
            next_page_url = response.url.replace("startPage={page_number}".format(page_number=startPage_match.group(1)),
                                                 "startPage={next_page_number}".format(next_page_number=int(startPage_match.group(1))+1))
            print("NEXT PAGE")
            print(next_page_url)
            if next_page_url is not None:
                yield scrapy.Request(next_page_url, callback=self.parse)
                # yield response.follow(next_page_url, self.parse)

    # def parse_job_details(self, response):
    #     def extract_with_css(query):
    #         return response.css(query).extract_first().strip()
    #
    #     yield {
    #         'name': extract_with_css('h3.author-title::text'),
    #         'birthdate': extract_with_css('.author-born-date::text'),
    #         'bio': extract_with_css('.author-description::text'),
    #     }

    def parse_job_details(self, response):
        print('parsing...')

        job_loader = ItemLoader(item=Job(), response=response)
        job_loader.add_value("crawled_at", str(datetime.now()))
        job_loader.add_xpath("categories",
                             "//div[@class='row job-info']//span[contains(@class, 'icon-plugin-1 icons')]/"
                             "parent::div/parent::div/div[@class='iconsiblings']/text()[normalize-space()]")
        job_loader.add_xpath("job_types",
                             "//div[@class='row job-info']//span[contains(@class, 'icons icon-briefcase')]/"
                             "parent::div/parent::div/div[@class='iconsiblings']//text()[normalize-space()]")
        job_loader.add_xpath("title", "//h1[@class='jobTitle']/text()")
        job_loader.add_xpath("job_date", "//li[@class='posted hidden-xs']/text()")
        job_loader.add_xpath("company", "//li[@class='employer']/a/text()")
        job_loader.add_xpath("company_url", "//li[@class='employer']/a/@href")
        # job_loader.add_xpath('description', '//div[@id="jobdescSec"]//text()')
        job_loader.add_xpath("location", "//li[@class='location']/text()")
        job_loader.add_value("provider", "dice")

        external_id = response.xpath(
            '//div[@class="company-header-info"]//div[contains(text(),"Position Id")]/text()').re(
            r'Position Id\s*:\s*(.*)')
        if external_id:
            job_loader.add_value('external_id', external_id[0])

        job_loader.add_xpath('url', '//link[@rel="canonical"]/@href')
        job_loader.add_xpath('image_urls',
                             "//div[contains(concat(' ', @class, ' '),' job-banner ')]//div[contains(@class,'bl-block')]/img/@src")
        job_loader.add_xpath('logo_urls',
                             "//div[contains(concat(' ', @class, ' '),' job-banner ')]//div[contains(@class,'brcs-logo')]//img/@src")
        job_loader.add_xpath('logo_urls',
                             "//div[contains(concat(' ', @class, ' '),' company-header-info ')]//img[contains(@class,'h-logo')]/@src")

        # l.add_xpath('name', '//div[@class="product_name"]')
        # l.add_xpath('name', '//div[@class="product_title"]')
        # l.add_xpath('price', '//p[@id="price"]')
        # l.add_css('stock', 'p#stock]')
        # l.add_value('last_updated', 'today')  # you can also use literal values

        yield job_loader.load_item()