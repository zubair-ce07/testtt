import scrapy
from scrapy.loader import ItemLoader
from Dice.items import Job
from datetime import datetime
import re
import urllib.parse as urlparse
from urllib.parse import urlencode


class DiceSpider(scrapy.Spider):
    name = "dice_spider"

    start_urls = [
        "https://www.dice.com/jobs?l=NY&startPage=1",
        "https://www.dice.com/jobs?l=CT&startPage=1"
    ]

    def parse(self, response):
        # follow links to job details page
        job_details_urls = response.xpath(
            "//div[@id='search-results-control']//a[contains(@id, 'position')]/@href").extract()
        if not job_details_urls:
            return

        for job_details_url in job_details_urls:
            yield scrapy.Request(job_details_url, callback=self.parse_job_details)

        yield self.request_next_page(response)

    @staticmethod
    def get_next_page_url(current_url):
        start_page_match = re.search("startPage=(\d+)", current_url)
        if start_page_match:
            current_page_no = int(start_page_match.group(1))
            start_page_param = {'startPage': current_page_no + 1}

            url_parts = list(urlparse.urlparse(current_url))
            query = dict(urlparse.parse_qsl(url_parts[4]))
            query.update(start_page_param)
            url_parts[4] = urlencode(query)

            next_page_url = urlparse.urlunparse(url_parts)
            return next_page_url

    def request_next_page(self, response):
        next_page_url = self.get_next_page_url(response.url)
        if next_page_url:
            return scrapy.Request(next_page_url, callback=self.parse)

    def parse_job_details(self, job_details_response):
        job_loader = ItemLoader(item=Job(), response=job_details_response)
        self.populate_categories(job_loader)
        self.populate_crawling_time(job_loader)
        self.populate_company_name(job_loader)
        self.populate_company_url(job_loader)
        self.populate_description(job_loader)
        self.populate_external_id(job_loader)
        self.populate_image_urls(job_loader)
        self.populate_job_date(job_loader)
        self.populate_job_types(job_loader)
        self.populate_location(job_loader)
        self.populate_logo_urls(job_loader)
        self.populate_provider(job_loader)
        self.populate_title(job_loader)
        self.populate_url(job_loader)

        yield job_loader.load_item()

    @staticmethod
    def populate_categories(job_loader):
        job_loader.add_xpath("categories",
                             "normalize-space(//*[@class='icon-plugin-1 icons']"
                             "//parent::div//following-sibling::div//text())")

    @staticmethod
    def populate_crawling_time(job_loader):
        job_loader.add_value("crawled_at", str(datetime.now()))

    @staticmethod
    def populate_company_name(job_loader):
        job_loader.add_xpath("company", "//li[@class='employer']/a/text()")

    @staticmethod
    def populate_company_url(job_loader):
        job_loader.add_xpath("company_url", "//li[@class='employer']/a/@href")

    @staticmethod
    def populate_description(job_loader):
        job_loader.add_xpath("description", "//div[@id='jobdescSec']//text()")

    @staticmethod
    def populate_external_id(job_loader):
        job_loader.add_xpath("external_id",
                             "normalize-space(substring-after(//div[@class='company-header-info'],'Position Id : '))")

    @staticmethod
    def populate_image_urls(job_loader):
        job_loader.add_xpath("image_urls",
                             "//div[contains(@class,'bl-block')]/img/@src")

    @staticmethod
    def populate_job_date(job_loader):
        job_loader.add_xpath("job_date", "//li[@class='posted hidden-xs']/text()")

    @staticmethod
    def populate_job_types(job_loader):
        job_loader.add_xpath("job_types",
                             "normalize-space(//*[@class='icons icon-briefcase']//parent::div//following-sibling::div)")

    @staticmethod
    def populate_location(job_loader):
        job_loader.add_xpath("location", "//li[@class='location']/text()")

    @staticmethod
    def populate_logo_urls(job_loader):
        job_loader.add_xpath("logo_urls",
                             "//div[contains(@class,'brcs-logo')]//img/@src | //img[contains(@class,'h-logo')]/@src")

    @staticmethod
    def populate_provider(job_loader):
        job_loader.add_value("provider", "dice")

    @staticmethod
    def populate_title(job_loader):
        job_loader.add_xpath("title", "//h1[@class='jobTitle']/text()")

    @staticmethod
    def populate_url(job_loader):
        job_loader.add_xpath("url", "//link[@rel='canonical']/@href")
