"""
This module scrapes quotes, aurhor_name, tags, image_url,
and social_media_url from brainy quotes website
"""
import json

import scrapy         #third party import although it is python framework

class QuotesSpider(scrapy.Spider):
    """
    This class in used to scrape the required data mentioned above
    """
    name = "quotes"
    pagination_url = 'https://www.brainyquote.com/api/inf'
    page = 1
    formdata = {
        'ab': 'b',
        'fdd': 'd',
        'id': 't:132622',
        'langc': 'en',
        'm': 0,
        'pg': 1,
        'typ': 'topic',
        'v': '8.3.4b:2915400',
        'vid': '7b363d749b4c7c684ace871c8a75f8e6'
    }


    def start_requests(self):
        """
        This method is execution point of scrapper that
        hits the given url with post request parameters
        :return:
        """
        yield scrapy.Request(url=self.pagination_url, body=json.dumps(self.formdata),
                             callback=self.parse, method='POST',
                             headers={'Content-Type': 'application/json'})


    def parse(self, response):
        """
        This method initiates when response is received. This method loads json
        format data from API and converts that data into HTML response for
        picking up required fields
        :param response:
        :return:
        """
        data = json.loads(response.body_as_unicode())
        new_response = data['content'].encode('ascii', 'ignore')
        sel1 = scrapy.Selector(text=new_response)
        for quote in sel1.css('div.m-brick'):
            yield {
                'quote': quote.css('a.b-qt::text').extract_first(),
                'author': quote.css('a.bq-aut::text').extract_first(),
                'tags': quote.css('a.oncl_k::text').extract(),
                'social_media_links': ['https://www.brainyquote.com' + link for link in
                                       quote.css('a.fa-stack::attr(href)').extract()],
                'image_url': 'https://www.brainyquote.com{}'.format(
                    quote.css('img.bqpht::attr(data-img-url)').extract_first())
            }
        self.page += 1
        self.formdata['pg'] = self.page
        yield scrapy.Request(url=self.pagination_url, body=json.dumps(self.formdata),
                             callback=self.parse, method='POST',
                             headers={'Content-Type': 'application/json'})

