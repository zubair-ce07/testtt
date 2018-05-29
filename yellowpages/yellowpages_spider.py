import os
import csv
import json
import urllib.parse

from scrapy.http import Request
from scrapy.spiders import CrawlSpider
from scrapylab.items import YellowPagesLoader


class YellowPages(CrawlSpider):
    name = 'yellowpages'
    allowed_domains = ['yellowpages.ca']
    start_urls = ['https://www.yellowpages.ca']

    def parse(self, response):
        categories = self.read_file(
            urllib.parse.urljoin('{}{}'.format(os.getcwd(), '/'), 'search-data/Categories_Generic.csv')
        )
        locations = self.read_file(
            urllib.parse.urljoin('{}{}'.format(os.getcwd(), '/'), 'search-data/canada_postal_codes.csv')
        )

        for category in categories:
            for location in locations:
                url = "search/si/1/{}/{}".format(category, location)
                request = Request(response.urljoin(url), callback=self.parse_urls)
                request.meta['search_category'] = category
                yield request

    def read_file(self, file_path):
        with open(file_path, "r") as file_content:
            csv.register_dialect('MyDialect', skipinitialspace=True)
            csv_reader = csv.DictReader(file_content, dialect='MyDialect')
            search_base = []

            for row in csv_reader:
                if 'postal' in file_path:
                    search_area = row["Province"]
                else:
                    search_area = row["Categories"]
                search_base.append(search_area)
            return search_base

    def parse_urls(self, response):
        yield self.pagination(response)
        product_urls = response.css('.listing__logo--link::attr(href)').extract()
        for url in product_urls:
            request = Request(response.urljoin(url), callback=self.parse_item)
            request.meta['search_category'] = response.meta['search_category']
            yield request

    def parse_item(self, response):
        loader = YellowPagesLoader(response=response)
        loader.add_value('url', response.url)
        loader.add_css('company_name', '.merchant-title__name::text')
        loader.add_css('telephone', '.mlr__sub-text::text')
        loader.add_css('address', '.merchant__address span::text')
        loader.add_xpath('postcode', '//*[@itemprop="postalCode"]//text()')
        loader.add_xpath('city', '//*[@itemprop="addressLocality"]//text()')
        loader.add_xpath('about_us', '//*[@itemprop="description"]//text()')

        xpath = '//*[@id="businessSection"]//*[contains(@class,"business__details")][h2/text()="\n{0}"]//ul//text()'
        loader.add_xpath('services', xpath.format('Services'))
        loader.add_xpath('products', xpath.format('Products and Services'))
        loader.add_xpath('associations', xpath.format('Association'))
        loader.add_xpath('specialties', xpath.format('Specialties'))

        loader.add_css('average_rating', '.merchant__rating::text')
        loader.add_css('review_content', '.review-content_text::text')
        loader.add_css('website', '.mlr__item--website .mlr__sub-text::text')

        raw_json = json.loads(response.xpath('//script[@id="reviews-config"]//text()').extract_first())
        loader.add_value('latitude', self.co_ordinates(raw_json.get('pins'), 'latitude'))
        loader.add_value('longitude', self.co_ordinates(raw_json.get('pins'), 'longitude'))

        if self.website(response):
            loader.add_value('website', response.urljoin(self.website(response)))

        loader.add_value('search_category', response.meta['search_category'])
        return loader.load_item()

    def website(self, response):
        return response.css('.mlr__item--website .mlr__item__cta::attr(href)').extract_first()

    def pagination(self, response):
        next_url = response.css('.yp-pagination__item--next a::attr(href)').extract_first()
        request = Request(response.urljoin(next_url), callback=self.parse_urls)
        request.meta['search_category'] = response.meta['search_category']
        return request

    def co_ordinates(self, raw_lat_lon, pin_val):
        for lat_lon in raw_lat_lon:
            return lat_lon.get(pin_val)
