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
    review_count_re = re.compile('(\d+)\s*reviews?|(\d+)\s+Google reviews?', flags=re.IGNORECASE)
    search_url = 'https://www.google.com.pk/search'

    def start_requests(self):
        fields = ['landmark', 'city' , 'region']

        with open('./spiders/top10-kayak_landmarks.csv') as csv:
            landmarks = DictReader(csv)
            yield from (self.search_request(landmark, fields) for landmark in landmarks)

    def search_request(self, landmark, fields):
        search_query = ' '.join([landmark[f] for f in fields])
        url = add_or_replace_parameter(self.search_url, 'q', search_query)
        return Request(url, callback=self.parse, meta={'record': landmark})

    def review_count(self, response):
        return clean(response.css('#rhs_block').re(self.review_count_re))[0]

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
        landmark['review_count'] = self.review_count(response)
        landmark['address'] = self.address(response)
        landmark['phone_number'] = self.phone_number(response)
        landmark['operating_hours'] = self.operating_hours(response)

        return landmark
