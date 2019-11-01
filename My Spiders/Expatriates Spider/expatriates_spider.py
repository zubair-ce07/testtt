from scrapy.spiders import Spider
from string import Template

from ..items import Classified
from ..utils import format_date


class ExpatriatesParseSpider():

    def parse_classified(self, response):
        classified = Classified()

        classified['name'] = self.get_name(response)
        classified['date'] = self.get_date(response)
        classified['category'] = self.get_category(response)
        classified['region'] = self.get_region(response) or response.css('new_region::text').get().strip()
        classified['classified_id'] = self.get_classified_id(response)
        classified['phone'] = self.get_phone(response)
        classified['description'] = self.get_description(response)
        classified['image_urls'] = self.get_image_urls(response)
        classified['url'] = self.get_url(response)

        yield classified

    def get_name(self, response):
        return response.css('.page-title h1::text').get().strip()

    def get_date(self, response):
        date = response.css('.post-info li').re_first(r'<strong>Date:</strong> (.*)</li>')
                
        return format_date(date, '%A, %B %d, %Y')

    def get_category(self, response):
        return response.css('.post-info li').re_first(r'<strong>Category:</strong> (.*)</li>')

    def get_region(self, response):
        return response.css('.post-info li').re_first(r'<strong>Region:</strong> (.*)</li>')

    def get_classified_id(self, response):
        return response.css('.post-info li').re_first(r'<strong>Posting ID:</strong> (.*)</li>')
    
    def get_phone(self, response):
        return int(response.css('.posting-phone a::text').get())

    def get_description(self, response):
        raw_description = [description.strip() for description in response.css('.post-body::text').getall()]

        return [description for description in raw_description if description]

    def get_image_urls(self, response):
        return response.css('.posting-images img::attr(src)').getall()

    def get_url(self, response):
        return response.url


class ExpatriatesCrawlSpider(Spider):
    name = 'expatriates_spider'
    allowed_domains = ['expatriates.com']
    start_urls = ['http://expatriates.com/classifieds/saudi-arabia/for-sale/']

    classified_parser = ExpatriatesParseSpider()

    url_template = Template('https://www.expatriates.com/classifieds/saudi-arabia/for-sale/index$page.html')

    def parse(self, response):
        pages_count = int(response.css('.pagination a::text').getall()[-2])

        for count in range(100, pages_count*100, 100):                        
            yield response.follow(self.url_template.substitute(page=count), callback=self.parse_listings)

    def parse_listings(self, response):        
        classified_urls = response.css('.listing-content a::attr(href)').getall()

        for url in classified_urls:
            yield response.follow(url, callback=self.parse_item)      

    def parse_item(self, response):        
        return self.classified_parser.parse_classified(response)        
