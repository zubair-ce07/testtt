from items import CourseLoader
from lxml import html
from urlparse import urljoin
import datetime
import re
import requests
import scrapy
import time


def concatenate_strings(a, b):
    if b == None:
        return None
    else:
        return '{}{}'.format(a, b)


class LyndaSpider(scrapy.Spider):
    name = "lynda_spider"
    start_urls = [
        'https://www.lynda.com/'
    ]

    def parse(self, response):
        for href in response.xpath('//div[@class="text-details"]//@href')\
                .extract():
            yield scrapy.Request(urljoin('https://www.lynda.com',
                                                  href), self.category)

    def category(self, response):
        category = response.xpath('//div[@id="category-page"]/@data-category-'
                                  'id').extract_first()
        page = 1
        while True:
            res = requests.get(concatenate_strings(concatenate_strings(
                concatenate_strings('https://www.lynda.com/ajax/category/'
                                 ,category),'/courses?page='),page))
            data = res.json()['html']
            if "role" in data:
                courses = re.findall(ur'href="(\S+)".+course-list', data)
                for course in courses:
                    yield scrapy.Request(course, self.parse_course)
            else:
                break
            page += 1

    def parse_course(self, response):
        course = CourseLoader(selector=response)
        course.add_xpath('author', '//cite[@data-ga-label="author-name"]'
                                   '/text()')
        course.add_xpath('categories', '//div[@class="tags subject-tags '
                                       'software-tags"]//text()')
        course.add_xpath('course_url', '//div[@id="embed-share-url"]'
                                       '/@data-course-url')
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
        price_page_tree = html.fromstring((requests.get(urljoin(
            'https://www.lynda.com',price_page))).content)
        premium_price = price_page_tree.xpath('//span[@class="premium"]'
                                              '/text()')[0][6:]
        course.add_value('premium_price', premium_price)
        basic_price = price_page_tree.xpath('//span[@class="basic"]'
                                            '/text()')[0][6:]
        course.add_value('basic_price', basic_price)
        course.add_value('provider', 'lynda')
        course.add_value('provider_url', 'https://www.lynda.com/')
        course.add_xpath('title', '//h1/@data-course')
        course.add_xpath('view_count', '//span[@id="course-viewers"]/text()')
        return course.load_item()
