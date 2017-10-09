# -*- coding: utf-8 -*-
import json
import re

from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class AnswerfinencialCrawlSpider(CrawlSpider):
    name = 'answerfinencial_crawl'
    allowed_domains = ['answerfinancial.com', 'api.bazaarvoice.com']
    start_urls = ['https://www.answerfinancial.com/']
    api_url_t = 'https://api.bazaarvoice.com/data/batch.json?passkey=u22jmac9b0y5a4g20u67tooka&apiversion=5.5&' \
                'resource.q0=reviews&filter.q0=productid:eq:{}&limit.q0=30&offset.q0={}'
    DEFAULT_OFFSET = 0
    product_id_re = re.compile(r'productId:\s+\"(.*)\"')

    rules = (
        Rule(LinkExtractor(restrict_css="#24", allow="CarrierPartner")),
        Rule(LinkExtractor(restrict_css=".pagination")),
        Rule(LinkExtractor(restrict_css=".partners-logo "), callback='parse_items_listing'),

    )
    secondry_ratings_map = {
        "Competitiveness": "Competitiveness of value",
        "Comfort": "Discounts offered",
        "Appearance1": "Quality of customer service",
        "Quality": "Quality of claims service"
    }

    def parse_items_listing(self, response):
        item = {}
        reviews_url = response.css('.reviews-link ::attr(href)').extract_first()
        name = response.css('.inner-title-main ::text').extract_first() or \
               response.css('.partner-view b:contains("About") ::text').extract_first()
        name = name.replace('About ', '')
        item['carrier_name'] = name
        if reviews_url:
            yield Request(url=reviews_url, callback=self.parse_reviews, meta={'item': item})

    def parse_reviews(self, response):
        item = response.meta['item']
        product_key = self.product_key(response)
        item['product_id'] = product_key
        item['carrier_rating'] = self.carrier_rating(response)
        item['url'] = response.url
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

            for page in range(30, int(total_reviews), 30):
                url = self.api_url_t.format(product_key, page)
                yield Request(url=url, callback=self.parse_reviews_api, meta={'item': item})

    def parse_item(self, item, response):
        item['submission_time'] = response['SubmissionTime']
        item['user_name'] = response['UserNickname'] or ''
        item['user_ratings'] = self.item_user_ratings(response)
        if response['UserLocation']:
            item['user_address'] = response['UserLocation']
        item['description'] = response['ReviewText']
        item['title'] = response['Title']

        item['secondary_ratings'] = dict()
        for key in response['SecondaryRatings'].keys():
            key_rating = self.secondry_ratings_map[key]
            item['secondary_ratings'][key_rating] = dict()
            item['secondary_ratings'][key_rating]['value'] = response['SecondaryRatings'][key]['Value']
            item['secondary_ratings'][key_rating]['ValueRange'] = response['SecondaryRatings'][key]['ValueRange']

        # item['raw_json'] = response

        return item

    def carrier_rating(self, response):
        ratings = dict()
        ratings['value'] = response.css('[itemprop="ratingValue"] ::text').extract_first()
        ratings['value_range'] = response.css('[itemprop="bestRating"] ::text').extract_first()
        return ratings

    def product_key(self, response):
        css = 'script:contains("productId")::text'
        return response.css(css).re_first(self.product_id_re)

    def item_user_ratings(self, response):
        user_ratings = dict()
        user_ratings['value'] = response['Rating']
        user_ratings['value_range'] = response['RatingRange']

        return user_ratings
