from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from linkedin.items import LinkedinProfileUrlItem
import re


class LinkedinSearchSpider(CrawlSpider):
    name = 'linkedin_search_spider'
    allowed_domains = ['www.linkedin.com']
    custom_settings = {'FEED_EXPORTERS': {'csv': 'scrapy.exporters.CsvItemExporter',},
                       'FEED_FORMAT': 'csv', 'FEED_URI': 'linkedin_urls%(time)s.csv'}

    rules = (
        Rule(LinkExtractor(
            restrict_css=['.bucket-list',
                          '.primary-section',
                          '.columns'], deny='https:\/\/www.linkedin.com\/in\/'),
            callback='parse_profile_search_results', follow=True),)

    def start_requests(self):
        return [Request("https://www.linkedin.com", callback=self.parse_linkedin, meta={'dont_cache': True})]

    def parse_linkedin(self, response):
        return Request(url='https://www.linkedin.com/directory/people-a/?trk=uno-reg-guest-home-people-directory',
                       meta={'dont_cache': True})

    def parse_profile_search_results(self, response):
        content_selector = response.css('.content')
        links = content_selector.css('a::attr(href)').extract()
        names = content_selector.css('a::text').extract()
        for link, name in zip(links, names):
            match = re.search('\/in\/', link)
            if match:
                linkedin_profile_url = LinkedinProfileUrlItem()
                linkedin_profile_url['url'] = response.urljoin(link)
                linkedin_profile_url['name'] = name
                yield linkedin_profile_url


