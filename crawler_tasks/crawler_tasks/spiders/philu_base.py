import json
import re
from urllib.parse import unquote

from scrapy.http import Request
from scrapy.selector import XPathSelector
from scrapy.spiders import Spider


def _sanitize(input_val):
    """ Shorthand for sanitizing results, removing unicode whitespace and normalizing end result"""
    if isinstance(input_val, XPathSelector):
        # caller obviously wants clean extracted version
        to_clean = input_val.extract()
    else:
        to_clean = input_val

    return re.sub('\s+', ' ', to_clean.replace('\xa0', ' ')).strip()


def clean(lst_or_str):
    """ Shorthand for sanitizing results in an iterable, dropping ones which would end empty """
    if not isinstance(lst_or_str, str) and getattr(lst_or_str, '__iter__', False):  # if iterable and not a string like
        return [x for x in (_sanitize(y) for y in lst_or_str if y is not None) if x]
    return _sanitize(lst_or_str)


def csrf_token(response):
    for cookie in response.headers.getlist('Set-Cookie'):
        match = re.match('XSRF-TOKEN=(.*);', cookie.decode())
        if match:
            return unquote(match.group(1))


def _course_id(url):
    return re.findall('.com\/([^\/]*)', url)[0]


class BaseSpider(Spider):
    name = 'philu-discussions'
    courses = [
        'https://philanthropyuniversity.novoed.com/capacity-2016-4/home',
        'https://philanthropyuniversity.novoed.com/scale-2017-1/home',
        'https://philanthropyuniversity.novoed.com/entrepreneurship-2017-1/home',
        'https://philanthropyuniversity.novoed.com/strategy-2017-1/home',
        'https://philanthropyuniversity.novoed.com/financial-modeling-2017-1/home',
        'https://philanthropyuniversity.novoed.com/leadership-2017-1/home',
        'https://philanthropyuniversity.novoed.com/fundraising-2017-1/home',
        'https://philanthropyuniversity.novoed.com/fundraising-2017-2/home'
    ]

    allowed_domains = [
        'novoed.com', 'cloudfront.net',
        'philanthropyuniversity.novoed.com'
    ]

    email = 'muhammad.zeeshan@arbisoft.com'
    password = 'CfR-c9C-Jh8-B7o'
    headers_with_cookies = {}

    def start_requests(self):
        url = 'https://app.novoed.com/my_account.json'
        meta = {
            'handle_httpstatus_list': [401],
            'dont_cache': True
        }
        return [Request(url, callback=self.sign_in_request, meta=meta)]

    def sign_in_request(self, response):
        payload = {
            'user': {
                'email': self.email,
                'password': self.password
            },
            'catalog_id': 'philanthropy-initiative'
        }
        url = 'https://app.novoed.com/users/sign_in.json'
        headers = {
            'Content-Type': 'application/json;charset=utf-8',
            'X-XSRF-TOKEN': csrf_token(response),
            'dont_cache': True
        }
        return Request(
            url, callback=self.parse_home_page, method='POST',
            body=json.dumps(payload), headers=headers)

    def parse_home_page(self, response):
        self.headers_with_cookies = {
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json, text/plain, */*',
            'X-CSRF-TOKEN': csrf_token(response)
        }

        yield from self.start_crawl(response)
