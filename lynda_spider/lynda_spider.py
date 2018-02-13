from items import CourseLoader
from urlparse import urljoin
import datetime
import json
import re
import scrapy
import time


class LyndaSpider(scrapy.Spider):
    name = 'lynda_spider'
    start_urls = [
        'https://www.lynda.com/subject/all'
    ]

    def parse(self, response):
        for href in response.xpath('//div[@class="software-name"]//@href')\
                .extract():
            yield scrapy.Request(urljoin('https://www.lynda.com',
                                                  href), self.extract_category)

    def extract_category(self, response):
        category = response.xpath('//div[@id="category-page"]/@data-category-'
                                  'id').extract_first()
        yield scrapy.Request('{}{}{}{}'.format('https://www.lynda.com/ajax/'
                                               'category/',category,'/courses?'
                                                                    'page=',1),
                             self.go_to_course)


    def go_to_course(self,response):
        data = json.loads(response.body)['html']
        page = int(response.url[-1])+1
        if "role" in data:
            courses = re.findall(ur'href="(\S+)".+course-list', data)
            for course in courses:
                yield scrapy.Request(course, self.parse_course)

            yield scrapy.Request(response.url[:-1] + str(page),
                                     self.go_to_course)


    def parse_course(self, response):
        course = CourseLoader(selector=response)
        course.add_xpath('author', '//cite[@data-ga-label="author-name"]'
                                   '/text()')
        course.add_xpath('categories', '//div[@class="tags subject-tags '
                                       'software-tags"]//text()')
        course.add_value('course_url', response.url)
        time_now = datetime.datetime.now().fromtimestamp(time.time()) \
            .strftime('%Y-%m-%d %H:%M:%S.%f')
        course.add_value('crawled_at', time_now)
        course.add_xpath('description', '//div[@itemprop="description"]'
                                        '//text()')
        course.add_xpath('duration', '//span[@itemprop="timeRequired"]'
                                     '/text()')
        course.add_xpath('external_id', '//div[@id="course-page"]'
                                        '/@data-course-id')
        course.add_xpath('level','//div[@class="course-info-stat-cont"]/h6'
                                 '/strong/text()')
        price_page =  response.xpath('//a[@class="btn tracking btn-action ga"'
                                     ' and @data-track-button="course-top-'
                                     'banner"]/@href').extract_first()
        course.add_value('provider', 'lynda')
        course.add_value('provider_url', 'https://www.lynda.com/')
        course.add_xpath('title', '//h1/@data-course')
        course.add_xpath('view_count', '//span[@id="course-viewers"]/text()')
        yield scrapy.Request(url=urljoin('https://www.lynda.com',price_page),
                             callback=self.parse_price,
                             meta={'item_loader':course})

    def parse_price(self, response):
        course = response.meta['item_loader']
        premium_price = response.xpath('//span[@class="premium"]'
                                       '/text()').extract_first()[6:]
        course.add_value('premium_price', premium_price)
        basic_price = response.xpath('//span[@class="basic"]'
                                     '/text()').extract_first()[6:]
        course.add_value('basic_price', basic_price)
        return course.load_item()
