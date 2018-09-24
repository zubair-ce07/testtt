import re
import json
from datetime import datetime

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Request, Rule

from ..items import PropertyItem
from .atira_property import PropertyParser


class AtiraSpider(CrawlSpider):

    name = "atira-crawl"

    start_urls = [
        'https://atira.com/why-atira/specials/'
    ]

    allowed_domains = ['atira.com']

    listing_css = ['.mobile-hide .ubermenu-target-with-image']

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse_location'),
    )

    deals = []

    parser = PropertyParser()

    def parse(self, response):
        self.deals = [response.css('.d-1of2 p::text').extract_first()]
        yield from super().parse(response)

    def parse_location(self, response):
        atira_property = PropertyItem()
        atira_property['deals'] = self.deals
        yield from self.features_request(response, atira_property)

    def parse_features(self, response):
        main_response = response.meta['main_response']
        atira_property = response.meta['a_property']
        atira_property['property_amenities'] = self.property_amenities(response)
        yield from self.room_requests(main_response, atira_property)

    def features_request(self, response, atira_property):
        feature_url = response.css('.grid-seemore ::attr(href)').extract_first()
        if feature_url:
            request = response.follow(url=feature_url, callback=self.parse_features)
            request.meta['main_response'] = response
            request.meta['a_property'] = atira_property
            yield request
        else:
            atira_property['deals'] = []
            atira_property['property_amenities'] = self.property_amenities(response)
            yield from self.room_requests(response, atira_property)

    def room_requests(self, response, atira_property):
        atira_property['property_contact_info'] = self.property_contact_info(response)
        atira_property['property_name'] = self.property_name(response)
        atira_property['landlord_slug'] = 'atira-student-living'
        atira_property['property_description'] = self.property_description(response)
        atira_property['property_images'] = self.property_images(response)
        atira_property['deposit_type'] = "fixed"
        atira_property['listing_type'] = "flexible_open_end"
        atira_property['deposit_amount'] = ""
        atira_property['deposit_name'] = "desposit"
        atira_property['property_ts_cs_url'] = ""
        atira_property['available_from'] = datetime.now().strftime("%d/%m/%Y")

        css = '#rooms .et_pb_image_sticky a::attr(href), .d-1of3 a::attr(href)'
        room_urls = response.css(css).extract()
        for url in room_urls:
            yield Request(url, callback=self.parser.parse, meta={'a_property': atira_property})

    def property_name(self, response):
        location_map = {'woolloongabba': 'Atira Woolloongabba', 'south-brisbane':
                        'Atira sth Brisbane', 'peel': 'Atira Peel', 'waymouth':
                        'Atira Waymouth', 'latrobe': 'Atira Latrobe', 'toowong':
                        'Atira Toowong'}
        for location in location_map:
            if location in response.url:
                return location_map[location]

    def property_description(self, response):
        css = '.et_pb_text_inner p::text, .entry-content p ::text'
        return [response.css(css).extract_first()]

    def property_contact_info(self, response):
        if response.css('.infowindow'):
            css = '.infowindow:contains("Atira") p ::text'
            contact_details = response.css(css).extract()
            return [detail.strip() for detail in contact_details]

        map_data = self.map_locations(response)
        location_details = json.loads(map_data)
        contact_details = location_details['infoWindows']
        for contact in contact_details:
            if contact['phone']:
                return [contact['phone'],
                        contact['email']]

    def map_locations(self, response):
        css = '.uber-google-map::attr(id)'
        map_id = response.css(css).extract_first()
        css = 'script:contains("UberGoogleMaps")'
        map_details = response.css(css).extract_first()
        pattern = re.compile(f"{map_id}'\)\.UberGoogleMaps\((.*?)\);")
        return pattern.findall(map_details)[0]

    def property_amenities(self, response):
        css = '#facilities .et_pb_blurb_description ::text, .d-1of4 p ::text'
        features = response.css(css).extract()
        features = [feat.strip() for feat in features if feat.strip()]
        return list(set(features))

    def property_images(self, response):
        css = '.et_pb_lightbox_image::attr(href)'
        image_urls = response.css('.slides li::attr(style)').extract()
        return [self.extract_image_url(url) for url in image_urls] or\
               response.css(css).extract()

    def extract_image_url(self, url_selector):
        return re.findall('url\((.*?)\)', url_selector)[0]
