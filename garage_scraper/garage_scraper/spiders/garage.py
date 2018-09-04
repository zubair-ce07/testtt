# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


class GarageSpider(scrapy.Spider):
    name = 'garage'
    allowed_domains = ['garageclothing.com']
    start_urls = ['http://garageclothing.com/ca']

    def start_requests(self):
        yield scrapy.Request(
            url='http://garageclothing.com/ca',
            callback=self.parse,
            cookies={
                'BVBRANDID': '81bcc6c1-fb49-4bd3-a63f-45db41195d16',
                'BVBRANDSID': 'e1ee1dd5-549f-4806-977d-655b450a9406',
                'BVImplmain_site': '14126',
                'JSESSIONID': 'pQM1sPCI70H3sldF9TqmRTk1.com9',
                '__cfduid': 'd0e148826908ab7de922943b74e1278cc1535971747',
                '_dc_gtm_UA-2391699-1': '1',
                '_ga': 'GA1.2.2094484639.1535971750',
                '_gat_UA-2391699-1': '1',
                '_gid': 'GA1.2.1407497093.1535971750',
                '_hjIncludedInSample': '1',
                '_scid': '5bfd6bd1-7189-4ff7-8600-4b3368449642',
                '_sctr': '1|1535914800000',
                'cto_lwid': '7edb2049-166e-4e59-9582-6d644c465c22',
                'geoipPrompt': 'true',
                'gig_hasGmid': 'ver2',
                'grgloyaltyca': 'true',
                'mp_groupe_dynamite_mixpanel': '%7B%22distinct_id%22%3A%20%221659f0d875941d-09b55e14eb9a25-3c720356-15f900-1659f0d875a9a2%22%7D',
                'optimizelyBuckets': '%7B%7D',
                'optimizelyEndUserId': 'oeu1535971757799r0.6048584038137765',
                'optimizelySegments': '%7B%222093613569%22%3A%22none%22%2C%222118004182%22%3A%22false%22%2C%222138484082%22%3A%22direct%22%2C%222140203178%22%3A%22gc%22%7D',
                'userPrefLanguage': 'en_CA'
            }
        )

    def parse(self, response):
        #from scrapy.shell import inspect_response
        #inspect_response(response, self)
        urls = response.css('div.zoomitem>a::attr(href)').extract()
        for url in urls:
            yield {
                'next_url': response.urljoin(url),
            }
