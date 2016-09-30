from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from linkedin_search.items import LinkedinProfilesItem
import re


class LinkedinSearchSpider(CrawlSpider):
    name = 'linkedin_search_spider'
    allowed_domains = ['www.linkedin.com']

    rules = (
        Rule(LinkExtractor(
            restrict_css=['.bucket-list',
                          '.primary-section',
                          '.columns'], deny='https:\/\/www.linkedin.com\/in\/'),
            callback='parse_profile_urls', follow=True),)

    def start_requests(self):
        return [Request("https://www.linkedin.com", callback=self.parse_search, meta={'dont_cache': True})]

    def parse_search(self, response):
        return Request(url='https://www.linkedin.com/directory/people-a/?trk=uno-reg-guest-home-people-directory',
                       meta={'dont_cache': True})

    def parse_profile_urls(self, response):
        links = response.xpath('//div[@class="content"]//a/@href | //li[@class="content"]//a/@href').extract()
        names = response.xpath('//div[@class="content"]//a/text() | //li[@class="content"]//a/text()').extract()
        for link, name in zip(links, names):
            match = re.search('\/in\/', link)
            if match:
                linkedin_profile = LinkedinProfilesItem()
                linkedin_profile['url'] = self.verify_url(link)
                linkedin_profile['name'] = name
                yield linkedin_profile

    def verify_url(self, link):
        match = re.search('https:\/\/www.linkedin.com\/in\/', link)
        if match:
            return link
        return 'https://www.linkedin.com' + link
