# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy import Selector
from w3lib.url import add_or_replace_parameter
from scrapy.spiders import Request


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


class LandmarkCrawlerSpider(scrapy.Spider):
    name = 'landmark_crawler'
    allowed_domains = ['google.com']
    google_review_re = re.compile('(\d+)\s*reviews?|([\d,]+)\s+Google reviews?', flags=re.IGNORECASE)
    trip_advisor_rating_re = re.compile('Rating:\s*[\d\.]+\s*-.*?([\d,]+) reviews', flags=re.IGNORECASE)
    search_url = 'https://www.google.com/search'

    def start_requests(self):
        fields = ['landmark', 'city']
        csv_path = './spiders/last-31K-landmarks.csv'
        self.logger.info(f'Reading landmarks from {csv_path}')

        with open(csv_path) as csv:
            landmarks = DictReader(csv)
            yield from (self.search_request(landmark, fields) for landmark in landmarks)

    def search_request(self, landmark, fields):
        search_query = ' '.join([landmark[f] for f in fields])
        url = add_or_replace_parameter(self.search_url, 'q', search_query)
        return Request(url, callback=self.parse, meta={'record': landmark})

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

    def parse(self, response):
        landmark = LandmarkcrawlerItem()

        landmark['url'] = response.url
        landmark['lmid'] = response.meta['record']['lmid']

        landmark['google_rating_count'] = self.google_rating_count(response)
        landmark['trip_advisor_rating_count'] = self.trip_advisor_rating_count(response)

        landmark['address'] = self.address(response)
        landmark['phone_number'] = self.phone_number(response)
        landmark['operating_hours'] = self.operating_hours(response)

        return landmark
