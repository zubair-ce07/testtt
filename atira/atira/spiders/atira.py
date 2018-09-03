import re
from datetime import datetime
from urllib.parse import urlparse

import json
from inline_requests import inline_requests
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule, Request

from ..items import PropertyItem
from .atira_property import PropertyParser


class AtiraSpider(CrawlSpider):

    name = "atira-crawl"
    start_urls = [
        'https://atira.com/'
    ]

    start_domain = urlparse(start_urls[0]).netloc

    listing_css = ['.mobile-hide .ubermenu-target-with-image']

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse_'),
    )

    property_parser = PropertyParser()

    @inline_requests
    def parse_(self, response):

        atira_property = PropertyItem()

        features_response = response
        deals_response = response

        if urlparse(response.url).netloc == self.start_domain:
            deals_url = response.xpath('/html/body/div[1]/header/div[2]/div[2]'
                                       '/nav/nav/ul/li[4]/a/@href').extract_first()
            deals_response = yield Request(deals_url, dont_filter=True)

            feature_url = response.css('.grid-seemore ::attr(href)').extract_first()
            features_response = yield Request(feature_url, dont_filter=True)

        atira_property['deals'] = self.property_deals(deals_response)
        atira_property['property_contact_info'] = self.property_contact_info(response)
        atira_property['property_name'] = self.property_name(response)
        atira_property['landlord_slug'] = 'atira-student-living'
        atira_property['property_description'] = self.property_description(response)
        atira_property['property_amenities'] = self.property_amenities(features_response)
        atira_property['property_images'] = self.property_images(response)
        atira_property['deposit_type'] = "fixed"
        atira_property['listing_type'] = "flexible_open_end"
        atira_property['deposit_amount'] = ""
        atira_property['deposit_name'] = "desposit"
        atira_property['property_ts_cs_url'] = ""
        atira_property['available_from'] = datetime.now().strftime("%d/%m/%Y")
        atira_property['room_type'] = "private-room"

        css = '#rooms .et_pb_image_sticky a::attr(href), .d-1of3 a::attr(href)'
        room_urls = response.css(css).extract()
        for url in room_urls:
            yield Request(url, callback=self.property_parser.parse, meta={'property': atira_property})

    def property_deals(self, response):
        deals = response.css('.d-1of2 p::text').extract()
        return [''.join(deals)]

    def property_name(self, response):
        location_map = {'woolloongabba': 'Atira Woolloongabba', 'south-brisbane':
                        'Atira sth Brisbane', 'peel': 'Atira Peel', 'waymouth':
                        'Atira Waymouth', 'latrobe': 'Atira Latrobe', 'toowong':
                        'Atira Toowong'}
        for location in location_map:
            if location in response.url:
                return location_map[location]
        return None

    def property_description(self, response):
        xpath = '/html/body/div[1]/div/div/article/div/div[1]/div/div/div[1]/div/p/text()'
        description = response.xpath(xpath).extract()
        css = '.et_pb_section_0 .et_pb_fullwidth_header_subhead::text, .entry-content.cf p *::text'
        description += response.css(css).extract()
        return [' '.join(description)]

    def property_contact_info(self, response):
        contacts = []
        map_id = response.css('.uber-google-map::attr(id)').extract_first()
        maps_data = response.xpath('//script[contains(text(), "UberGoogleMaps")]/text()').extract_first()
        if not maps_data:
            return contacts

        maps_locations = maps_data.split(';')
        location_details = ""
        for location in maps_locations:
            if map_id in location:
                location_details = location[location.find('{'):-1]

        location_details = json.loads(location_details)
        contact_details = location_details['infoWindows']
        for contact in contact_details:
            if contact['phone']:
                contacts.append(contact['phone'])
                contacts.append(contact['email'])

        return contacts

    def property_amenities(self, response):
        css = '#facilities .et_pb_blurb_description ::text'
        features = response.css(css).extract()
        features += response.css('.d-1of4 p *::text').extract()
        return [feat.strip() for feat in features if feat.strip()]

    def property_images(self, response):
        image_urls = response.css('.slides li::attr(style)').extract()
        return [self.extract_image_url(url) for url in image_urls]

    def extract_image_url(self, url_selector):
        return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]'
                          '|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url_selector)[0]
