# -*- coding: utf-8 -*-
import json
import datetime
import scrapy


class SafeAutoSpider(scrapy.Spider):
    name = 'safe_auto'
    allowed_domains = ['safeauto.com', 'powerreviews.com']
    start_urls = ['https://safeauto.com/about/reviews']
    headers = {
        'authorization': 'e7c4f2de-5e12-45e2-b345-5305a1afac90',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,'
                      ' like Gecko) Chrome/63.0.3239.108 Safari/537.36'
    }

    def parse(self, response):
        paging_url = 'https://readservices-b2c.powerreviews.com/m/226561/l/en_US/product/insurance/reviews?'

        yield scrapy.Request(url=paging_url, headers=self.headers, callback=self.parse_reviews)

    def parse_reviews(self, response):
        api_data = json.loads(response.text)
        next_page_url = api_data['paging']['next_page_url']
        next_page_url.replace('paging.size=10', 'paging.size=25')
        yield scrapy.Request(url=response.urljoin(next_page_url), headers=self.headers, callback=self.parse_reviews)
        for review in api_data['results'][0]['reviews']:
            item = {
                'title': review['details']['headline'],
                'name': review['details']['nickname'],
                'location': review['details']['location'],
                'rating': review['metrics']['rating'],
                'total_rating': 5,
                'text': review['details']['comments'],
                'date': '',
                'pros': [],
                'cons': []
            }
            date = str(review['details']['created_date'])
            item['date'] = datetime.datetime.fromtimestamp(int(date[:-3])).strftime('%Y-%m-%d %H:%M:%S')

            for property in review['details']['properties']:
                if property['key'] == 'pros':
                    item['pros'] = property['value']
                if property['key'] == 'cons':
                    item['cons'] = property['value']

            yield item
