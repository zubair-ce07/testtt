from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from linkedin.items import LinkedinProfileUrlItem
import re


class LinkedinSearchSpider(CrawlSpider):
    name = 'linkedin_search_spider'
    allowed_domains = ['www.linkedin.com']
    custom_settings = {'FEED_EXPORTERS': {'csv': 'scrapy.exporters.CsvItemExporter',},
                       'FEED_FORMAT': 'csv', 'FEED_URI': 'linkedin_urls_%(time)s.csv'}

    rules = (
        Rule(LinkExtractor(
            restrict_css=['.bucket-list',
                          '.primary-section',
                          '.columns'], deny=r'https://www.linkedin.com/in/'),
            callback='parse_profile_search_results', follow=True),)

    def start_requests(self):
        return [Request("https://www.linkedin.com", callback=self.parse_linkedin, meta={'dont_cache': True})]

    def parse_linkedin(self, response):
        return Request(url='https://www.linkedin.com/directory/people-a/?trk=uno-reg-guest-home-people-directory',
                       meta={'dont_cache': True}, dont_filter=True)

    def parse_profile_search_results(self, response):
        if response.status == 999:
            return self.retry_request(response)
        self.logger.info(response.request.meta['proxy'])
        url = response.url
        # check for mulitple profiles for one name
        mulitple_profiles = re.search(r'/pub/dir/', url)
        content_selectors_css = '.content'
        if mulitple_profiles:
            content_selectors_css = 'div[class="content"] h3'
        content_selectors = response.css(content_selectors_css)
        for content_selector in content_selectors:
            link = content_selector.css('a::attr(href)').extract_first()
            match = re.search(r'/in/', link)
            if match:
                linkedin_profile_url = LinkedinProfileUrlItem()
                linkedin_profile_url['url'] = response.urljoin(link)
                linkedin_profile_url['name'] = content_selector.css('a::text').extract_first()
                yield linkedin_profile_url

    def retry_request(self, response):
        retries = response.meta.get('retries', 0)
        retries += 1
        if retries > 5:
            args = (5, response.url)
            self.logger.warning('Failed %d times on %s. Giving up.' % args)
            return
        else:
            response.request.meta['retries'] = retries
            response.request.dont_filter = True
            return response.request
