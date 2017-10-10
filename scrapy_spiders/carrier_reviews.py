import json
import re

import scrapy
from w3lib.url import add_or_replace_parameter


class CarrierReviews(scrapy.Spider):
    name = "carriers"
    json_api_start = "https://api.bazaarvoice.com/data/batch.json?passkey=u22jmac9b0y5a4g20u67tooka&" \
                     "apiversion=5.5"
    json_api_key = "p_PRO_FAMILY"
    json_api_ratings = "&filteredstats.q0=reviews&resource.q0=products&filter.q0=id%3Aeq%3A"
    json_api_reviewer = '&filteredstats.q1=reviews&resource.q1=reviews&limit.q1=100' \
                        '&offset.q1={0}&filter.q1=productid%3Aeq%3A'
    start_urls = ['https://www.answerfinancial.com/AboutUs/CarrierPartner/1?a=RETAIL']

    required_data = {}

    def parse(self, response):
        for link in response.css('div.reviews-link a::attr(href)'):
            yield response.follow(link, self.parse_carrier)
            # for link in response.css('div.pager-block a::attr(href)').extract()[-1]:
            #    if link:
            #        yield response.follow(link, self.parse)

    def parse_carrier(self, response):
        carrier_name = response.css('div.main-title h1::text').extract_first()
        script = response.css('script[type="text/javascript"]::text').extract_first()
        self.json_api_key = re.search(r'p_[A-Z]{3}_FAMILY', script).group(0)
        company = {
            'Carrier Name': carrier_name,
            'Overall Ratings': response.css('span.bvseo-ratingValue::text').extract_first(),
            'reviews': []
        }
        json_api_url = '{}{}{}'.format(self.json_api_start,
                                       self.json_api_reviewer.format(0),
                                       self.json_api_key)
        yield scrapy.http.Request(url=json_api_url, callback=self.parse_json, meta={'offset': 0, 'company': company})

        # for review in response.css('div.bvseo-review'):
        #    yield{
        #        'Author': review.css('span[itemprop="author"]::text').extract_first(),
        #        'Date Published': review.css('meta[itemprop="datePublished"]::attr(content)').extract_first(),
        #        'Review Text': review.css('span[itemprop="name"]::text').extract_first()
        #    }
        # link = response.css('a.bvseo-paginationLink::attr(href)').extract_first()
        # if link:
        #    yield response.follow(link, self.parse_carrier)

    def parse_json(self, response):
        company = response.meta['company']
        json_data = json.loads(response.text)
        filtered_reviews = json_data['BatchedResults']['q1'].get('Results', [])
        # implement a for loop for all reviews in results and increment offset..
        for raw_review in filtered_reviews:
            review = {
                'name': raw_review.get('UserNickname', 'anonymous'),
                'city/state': raw_review.get('UserLocation', 'N/A'),
                'quality_of_service': raw_review['SecondaryRatings'].get('Quality', {'Value': 'N/A'})['Value'],
                'date': raw_review.get('SubmissionTime', 'N/A'),
                'description': raw_review.get('Title', 'N/A'),
                'competitiveness': raw_review['SecondaryRatings'].get('Competitiveness', {'Value': 'N/A'})['Value'],
                'discounts': raw_review['SecondaryRatings'].get('Comfort', {'Value': 'N/A'})['Value'],
            }
            company['reviews'].append(review)
        if filtered_reviews:
            offset = int(response.meta['offset']) + 100
            url = add_or_replace_parameter(response.url, 'offset.q1', offset)
            yield scrapy.Request(url=url, callback=self.parse_json, meta={'offset': offset, 'company': company})
        else:
            yield company
