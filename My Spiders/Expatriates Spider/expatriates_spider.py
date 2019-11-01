from scrapy.spiders import Spider
from datetime import datetime
from string import Template

from ..items import Classified


class ExpatriatesParseSpider():

    def parse_classified(self, response):
        classified = Classified()

        classified['name'] = self.get_name(response)
        classified['date'] = self.get_date(response)
        classified['category'] = self.get_category(response)
        classified['region'] = self.get_region(response)
        classified['classified_id'] = self.get_classified_id(response)
        classified['phone'] = self.get_phone(response)
        classified['description'] = self.get_description(response)
        classified['image_urls'] = self.get_image_urls(response)
        classified['url'] = self.get_url(response)

        return classified

    def get_name(self, response):
        return response.css('.page-title h1::text').get().strip()

    def get_date(self, response):
        date = response.css('.post-info li').re_first(r'<strong>Date:</strong> (.*)</li>')
                
        return self.format_date(date, '%A, %B %d, %Y')

    def get_category(self, response):
        return response.css('.post-info li').re_first(r'<strong>Category:</strong> (.*)</li>')

    def get_region(self, response):
        region = response.css('.post-info li').re_first(r'<strong>Region:</strong> (.*)</li>')

        return region if region else response.css('new_region::text').get().strip()

    def get_classified_id(self, response):
        return response.css('.post-info li').re_first(r'<strong>Posting ID:</strong> (.*)</li>')
    
    def get_phone(self, response):
        phone = response.css('.posting-phone a::text').get()
        
        return int(phone) if phone else ''

    def get_description(self, response):        
        return [description.strip() for description in response.css('.post-body::text').getall()][:-2]

    def get_image_urls(self, response):
        return response.css('.posting-images img::attr(src)').getall()

    def get_url(self, response):
        return response.url

    def format_date(self, date, date_format):
        return datetime.strptime(date, date_format).date()


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
        classified_urls = [url for url in response.css('.listing-content a::attr(href)').getall() if '/cls' in url]

        for url in classified_urls:
            yield response.follow(url, callback=self.parse_item)      

    def parse_item(self, response):        
        return self.classified_parser.parse_classified(response)        
