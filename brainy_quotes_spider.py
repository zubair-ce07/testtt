import scrapy
import json


class BrainyQuotesSpider(scrapy.Spider):
    name = "BrainyQuotes"
    start_urls = [
         'https://www.brainyquote.com/topics/motivational'
     ]
    request_url = 'https://www.brainyquote.com/api/inf'

    page = 1
    request_params = {
        'ab': 'a',
        'fdd': 'd',
        'id': 't:132622',
        'langc': 'en',
        'm': 0,
        'pg': 1,
        'typ': 'topic',
        'v': '8.4.0b:2951607',
        'vid': '7b363d749b4c7c684ace871c8a75f8e6'
    }

    def parse(self, response):
        for quotes in response.css('div.m-brick'):
            yield {
                    'Quote': quotes.css('div.clearfix a.b-qt::text').extract_first(),
                    'Author': quotes.css('div.clearfix a.oncl_a::text').extract_first(),
                    'Tags': quotes.css('div.kw-box a.oncl_list_kc::text').extract(),
                    'Shareable links': quotes.css('div.sh-box a.fa-stack::attr(href)').extract(),
                    'img_url': quotes.css('div.qti-listm img.zoomc::attr(data-img-url)').extract_first(),
            }

        self.page += 1
        self.request_params['pg'] = self.page
        yield scrapy.Request(self.request_url, callback=self.parse_scrolled_pages, method='POST', body=json.dumps(self.request_params),
                             headers={'Content-Type': 'application/json'})

    def parse_scrolled_pages(self, response):
        json_response = json.loads(response.body_as_unicode())
        data_store = json_response['content'].encode('ascii', 'ignore')
        data = scrapy.Selector(text=data_store)
        for quotes in data.css('div.m-brick'):
            yield {
                    'Quote': quotes.css('div.clearfix a.b-qt::text').extract_first(),
                    'Author': quotes.css('div.clearfix a.oncl_a::text').extract_first(),
                    'Tags': quotes.css('div.kw-box a.oncl_list_kc::text').extract(),
                    'Shareable links': quotes.css('div.sh-box a.fa-stack::attr(href)').extract(),
                    'img_url': quotes.css('div.qti-listm img.zoomc::attr(data-img-url)').extract_first(),
            }
        self.page += 1
        self.request_params['pg'] = self.page
        yield scrapy.Request(self.request_url, callback=self.parse_scrolled_pages, method='POST',
                             body=json.dumps(self.request_params),
                             headers={'Content-Type': 'application/json'})


