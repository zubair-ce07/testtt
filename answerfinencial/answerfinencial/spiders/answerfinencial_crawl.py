# -*- coding: utf-8 -*-
import json
import re

from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class AnswerfinencialCrawlSpider(CrawlSpider, Base):
    name = 'answerfinencial_crawl'
    allowed_domains = ['answerfinancial.com', 'api.bazaarvoice.com']
    start_urls = ['https://www.answerfinancial.com/']
    api_url_t = 'https://api.bazaarvoice.com/data/batch.json?passkey=u22jmac9b0y5a4g20u67tooka&apiversion=5.5&' \
                'resource.q0=reviews&filter.q0=productid:eq:{}&limit.q0=30&offset.q0={}'
    DEFAULT_OFFSET = 8
    product_id_re = re.compile(r'productId:\s+\"(.*)\"')

    rules = (
        Rule(LinkExtractor(restrict_css="#24", allow="CarrierPartner")),
        Rule(LinkExtractor(restrict_css=".pagination")),
        Rule(LinkExtractor(restrict_css=".partners-logo "), callback='parse_items_listing'),

    )

    def parse_items_listing(self, response):
        item = {}
        reviews_url = response.css('.reviews-link ::attr(href)').extract_first()
        name = response.css('.inner-title-main ::text').extract_first() or \
               response.css('.partner-view b:contains("About") ::text').extract_first()
        name = name.replace('About ', '')
        item['Carrier_name'] = name
        if reviews_url:
            yield Request(url=reviews_url, callback=self.parse_reviews, meta={'item': item})

    def parse_reviews(self, response):
        item = response.meta['item']
        product_key = self.product_key(response)

        item['product_id'] = product_key
        api_url = self.api_url_t.format(product_key, self.DEFAULT_OFFSET)
        yield Request(url=api_url, meta={'item': item}, callback=self.parse_reviews_api)

    def parse_reviews_api(self, response):
        item = response.meta['item']
        reviews = json.loads(response.text)
        total_reviews = reviews['BatchedResults']['q0']['TotalResults']

        for review in reviews['BatchedResults']['q0']['Results']:
            yield self.parse_item(item, review)

        reviews_offset = int(reviews['BatchedResults']['q0']['Offset'])
        print(reviews_offset)
        if reviews_offset == self.DEFAULT_OFFSET:
            product_key = item['product_id']

            for page in range(self.DEFAULT_OFFSET + 30, int(total_reviews), 30):
                url = self.api_url_t.format(product_key, page)
                yield Request(url=url, callback=self.parse_reviews_api, meta={'item': item})

    def parse_item(self, item, response):
        item['SubmissionTime'] = response['SubmissionTime']
        item['user'] = dict()
        item['user']['name'] = response['UserNickname'] or ''
        if response['UserLocation']:
            if ',' in response['UserLocation']:
                item['user']['city'] = response['UserLocation'].split(',')[0]
                item['user']['state'] = response['UserLocation'].split(',')[1]
            else:
                item['user']['state'] = response['UserLocation']
        item['description'] = response['ReviewText']

        item['SecondaryRatings'] = dict()
        for key in response['SecondaryRatings'].keys():
            item['SecondaryRatings'][key] = dict()
            item['SecondaryRatings'][key]['value'] = response['SecondaryRatings'][key]['Value']
            item['SecondaryRatings'][key]['ValueRange'] = response['SecondaryRatings'][key]['ValueRange']

        # item['raw_json'] = response

        return item

    def product_key(self, response):
        css = 'script:contains("productId")::text'
        return response.css(css).re_first(self.product_id_re)
