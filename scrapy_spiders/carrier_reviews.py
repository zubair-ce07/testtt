import json
import re
from datetime import datetime

from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from w3lib.url import add_or_replace_parameter


class CarrierReviews(CrawlSpider):
    name = "carriers"
    api_base_link = 'https://api.bazaarvoice.com/data/batch.json?' \
                    'passkey=u22jmac9b0y5a4g20u67tooka&apiversion=5.5' \
                    '&filteredstats.q1=reviews&resource.q1=reviews&limit.q1=100' \
                    '&offset.q1=0&filter.q1=productid%3Aeq%3A{}'

    start_urls = ['https://www.answerfinancial.com/AboutUs/CarrierPartner/1?a=RETAIL']

    listing_css = '.pager-block'
    carrier_css = '.reviews-link'

    rules = (
                Rule(LinkExtractor(restrict_css=listing_css)),
                Rule(LinkExtractor(restrict_css=carrier_css), callback='parse_carrier'),
        )

    def parse_carrier(self, response):
        carrier_name = response.css('.main-title h1::text').extract_first()
        overall_ratings = response.css('span.bvseo-ratingValue::text').extract_first()
        raw_company_id = response.css('script[type="text/javascript"]::text').extract_first()
        company_id = re.search(r'p_[A-Z]{3}_FAMILY', raw_company_id).group(0)

        company = {
            'Carrier Name': carrier_name,
            'Overall Ratings': overall_ratings
        }

        meta_data = {'offset': 0, 'company': company}
        json_api_url = self.api_base_link.format(company_id)
        return Request(url=json_api_url, callback=self.parse_reviews, meta=meta_data)

    def parse_reviews(self, response):
        company = response.meta['company']
        reviews_response = json.loads(response.text)
        company_reviews = reviews_response['BatchedResults']['q1'].get('Results', [])
        date_time_format = "%Y-%m-%dT%H:%M:%S.%f+00:00"

        for raw_review in company_reviews:
            review_ratings = raw_review['SecondaryRatings']

            review_date = datetime.strptime(raw_review.get('SubmissionTime'), date_time_format).date()
            competitiveness = review_ratings.get('Competitiveness', {'Value': 'N/A'})['Value']
            discounts = review_ratings.get('Comfort', {'Value': 'N/A'})['Value']
            quality_of_service = review_ratings.get('Quality', {'Value': 'N/A'})['Value']

            review = {
                'author_name': raw_review.get('UserNickname', 'Anonymous'),
                'city/state': raw_review.get('UserLocation', 'N/A'),
                'title': raw_review.get('Title', 'N/A'),
                'description': raw_review.get('ReviewText', 'N/A'),
                'date': review_date,
                'competitiveness': competitiveness,
                'discounts': discounts,
                'quality_of_service': quality_of_service,
            }
            company['reviews'].append(review)

        if company_reviews:
            offset = int(response.meta['offset']) + 100
            api_next_link = add_or_replace_parameter(response.url, 'offset.q1', offset)
            meta_data = {'offset': offset, 'company': company}
            return Request(url=api_next_link, callback=self.parse_reviews, meta=meta_data)
        else:
            return company
