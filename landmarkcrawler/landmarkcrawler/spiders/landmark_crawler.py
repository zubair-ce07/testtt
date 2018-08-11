# -*- coding: utf-8 -*-
import json
import re

import scrapy
from scrapy import Selector
from w3lib.url import add_or_replace_parameter
from scrapy import Request
from urllib.parse import urljoin
from csv import DictReader

from ..items import LandmarkcrawlerItem


def _sanitize(input_val):
    if isinstance(input_val, Selector):
        to_clean = input_val.extract()
    else:
        to_clean = input_val

    return re.sub('\s+', ' ', to_clean.replace('\xa0', ' ')).strip()


def clean(lst_or_str):
    if not isinstance(lst_or_str, str) and getattr(lst_or_str, '__iter__', False):
        return [x for x in (_sanitize(y) for y in lst_or_str if y is not None) if x]
    return _sanitize(lst_or_str)

def reset_cookies(request):
    request.meta['dont_merge_cookies'] = True
    request.cookies = {}
    return request


class LandmarkCrawlerSpider(scrapy.Spider):
    name = 'landmark_crawler'
    allowed_domains = ['google.com', 'www.tripadvisor.com', 'google.com.pk']
    google_review_re = re.compile('(\d+)\s*reviews?|([\d,]+)\s+Google reviews?', flags=re.IGNORECASE)
    trip_advisor_rating_re = re.compile('Rating:\s*[\d\.]+\s*-.*?([\d,]+) reviews', flags=re.IGNORECASE)
    search_url = 'https://www.google.com/search'

    def start_requests(self):
        csv_path = './landmarkcrawler/new_file.csv'
        fields = ['landmark', 'city']
        self.logger.info(f'Reading landmarks from {csv_path}')
        with open(csv_path) as csv:
            landmarks = DictReader(csv)
            yield from (self.search_request(landmark, fields) for landmark in landmarks)


    # def start_requests(self):
    #     yield Request('https://www.google.com/', callback=self.parse_from_file)
    #
    # def parse_from_file(self, response):
    #     csv_path = './landmarkcrawler/kayak_landmarks.csv'
    #     json_path = './landmarkcrawler/new_file.json'
    #     self.logger.info(f'Reading landmarks from {csv_path}')
    #
    #     with open(csv_path) as f:
    #         landmarks = json.load(f)
    #         yield from (self.google_search_request(landmark) for landmark in landmarks)

    def google_search_request(self, landmark, fields, landmark_item):
        exact_match = landmark[fields[0]]
        any_words = landmark[fields[1]]
        url = add_or_replace_parameter(self.search_url, 'as_q', any_words)
        url = add_or_replace_parameter(url, 'as_epq', exact_match)
        url = add_or_replace_parameter(url, 'as_sitesearch', 'tripadvisor.com')
        return reset_cookies(Request(url, callback=self.parse_landmark, meta={'use_proxy': True, 'landmark': landmark_item}))

    def search_request(self, landmark, fields):
        search_query = ' '.join([landmark[f] for f in fields])
        url = add_or_replace_parameter(self.search_url, 'q', search_query)
        return reset_cookies(Request(url, callback=self.parse, meta={'use_proxy': True, 'record': landmark, 'fields': fields}))

    def google_rating_count(self, response):
        rating = response.css('#rhs_block').re(self.google_review_re)

        if not rating:
            return None

        rating = clean(rating)[0].replace(',', '')
        return int(rating)

    def trip_advisor_rating_count(self, response):
        xpath = '//*[@id="rso"]//*[.//g-review-stars and @data-ved and contains(., "tripadvisor")]'
        sel = response.xpath(xpath)

        if not sel:
            return None

        rating = clean(sel.re(self.trip_advisor_rating_re)) or ['1']
        return int(rating[0].replace(',', ''))

    def address(self, response):
        css = '[data-local-attribute="d3adr"] .LrzXr ::text'
        xpath = '//*[@id="rhs_block"]//*[@class="V7Q8V" and contains(., "Address")]' \
                '//*[@class="A1t5ne"]//text()'
        return (clean(response.css(css)) or clean(response.xpath(xpath)) or [''])[0]

    def phone_number(self, response):
        css = '[data-local-attribute="d3ph"] .LrzXr ::text'
        xpath = '//*[@id="rhs_block"]//*[@class="V7Q8V" and contains(., "Phone")]' \
                '//*[@class="A1t5ne"]//text()'
        return (clean(response.css(css)) or clean(response.xpath(xpath)) or [''])[0]

    def operating_hours(self, response):
        css = '[data-local-attribute="d3oh"] tr'
        return [': '.join(clean(sel.css('::text'))) for sel in response.css(css)]

    def get_title(self, response):
        xpath = '//*[@id="rso"]//*[.//g-review-stars and @data-ved and contains(., "tripadvisor")]//h3/a/text()'
        return (clean(response.xpath(xpath)) or [''])[0]

    def get_trip_advisor_url(self, response):
        xpath = '//*[@id="rso"]//*[.//g-review-stars and @data-ved and contains(., "tripadvisor")]//h3/a/@href'
        return (clean(response.xpath(xpath)) or [''])[0]

    def trip_advisor_reviews_count(self, response):
        css = '.reviews_header_count::text'
        return int((clean(response.css('.rating_and_popularity .rating [property="count"]::text')) or
                    [''.join(clean(response.css(css).re('\d+')))])[0])

    def trip_advisor_heading(self, response):
        return (clean(response.css('.heading_title ::text, #PAGEHEADING::text, #HEADING::text')) or
                clean(response.css('.ui_column.wrap_column.meta-block-header')) or [''])[0]

    def is_no_result_tag(self, response):
        xpath = '//div[contains(text(), "No results found for ")] |' \
                ' //p[contains(., " - did not match any documents.  ")]'

        return True if clean(response.xpath(xpath)) else False

    def trip_advisor_title(self, response):
        return (clean(response.css('head title::text')) or [''])[0]

    def parse(self, response):
        landmark = LandmarkcrawlerItem()

        landmark['google_search_url'] = response.url
        landmark['lmid'] = response.meta['record']['lmid']
        landmark['google_rating_count'] = self.google_rating_count(response)
        landmark['address'] = self.address(response)
        landmark['phone_number'] = self.phone_number(response)
        landmark['operating_hours'] = self.operating_hours(response)
        landmark['google_search_title'] = self.get_title(response)

        return self.google_search_request(response.meta['record'], response.meta.get('fields'), landmark)

        # ta_count = self.trip_advisor_rating_count(response)
        # url = self.get_trip_advisor_url(response)
        #
        # if ta_count and ta_count > 1:
        #     landmark['trip_advisor_url'] = url
        #     landmark['trip_advisor_rating_count'] = self.trip_advisor_rating_count(response)
        #     return landmark
        #
        # if not url:
        #     url = f'{landmark["google_search_url"]}+tripadvisor'
        #     return Request(url, callback=self.parse_landmark,
        #                    meta={'landmark': landmark, 'use_proxy': True})
        #
        # url = urljoin('https://', url)
        # return Request(url, callback=self.parse_trip_advisor, meta={'landmark': landmark, 'use_proxy': False})

    def parse_landmark(self, response):
        landmark = response.meta.get('landmark')
        landmark['google_advance_search_url'] = response.url
        landmark['google_search_title'] = self.get_title(response)

        if self.is_no_result_tag(response):
            landmark['trip_advisor_rating_count'] = None
            landmark['trip_advisor_url'] = None
            landmark['trip_advisor_heading'] = None
            landmark['trip_advisor_page_title'] = None
            return landmark

        url = self.get_trip_advisor_url(response)

        if not url:
            landmark['trip_advisor_rating_count'] = None
            landmark['trip_advisor_url'] = None
            landmark['trip_advisor_heading'] = None
            landmark['trip_advisor_page_title'] = None
            return landmark

        return reset_cookies(Request(url, callback=self.parse_trip_advisor, meta={'landmark': landmark, 'use_proxy': False}))

        # ta_count = self.trip_advisor_rating_count(response)
        #
        # url = self.get_trip_advisor_url(response)
        #
        # if ta_count and ta_count > 1:
        #     landmark['trip_advisor_url'] = url
        #     landmark['trip_advisor_rating_count'] = self.trip_advisor_rating_count(response)
        #     return landmark
        #
        # landmark['trip_advisor_url'] = url
        # url = urljoin('https://', url)
        # return Request(url, callback=self.parse_trip_advisor, meta={'landmark': landmark, 'use_proxy': False})

    def parse_trip_advisor(self, response):
        landmark = response.meta.get('landmark')

        landmark['trip_advisor_url'] = response.url
        landmark['trip_advisor_heading'] = self.trip_advisor_heading(response)
        landmark['trip_advisor_page_title'] = self.trip_advisor_title(response)

        if clean(response.css('.global-nav-link.ui_tab.active::attr(data-tracking-label)'))[0] == 'attractions':
            landmark['trip_advisor_rating_count'] = self.trip_advisor_reviews_count(response)
        else:
            landmark['trip_advisor_rating_count'] = None

        return landmark
