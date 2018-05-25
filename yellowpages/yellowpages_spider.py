import os
import csv
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
        postal_codes = self.read_file(
            urllib.parse.urljoin('{}{}'.format(os.getcwd(), '/'), 'search-data/canada_postal_codes.csv')
        )

        for category in categories:
            for postal_code in postal_codes:
                url = "search/si/1/{}/{}".format(category, postal_code)
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
        product_urls = response.css('a.listing__logo--link::attr(href)').extract()
        for url in product_urls:
            request = Request(response.urljoin(url), callback=self.parse_item)
            request.meta['search_category'] = response.meta['search_category']
            yield request

    def parse_item(self, response):
        yellowpages_loader = YellowPagesLoader(response=response)
        yellowpages_loader.add_value('url', response.url)
        yellowpages_loader.add_css('company_name', 'span.merchant-title__name::text')
        yellowpages_loader.add_css('telephone', 'span.mlr__sub-text::text')
        yellowpages_loader.add_css('address', 'div.merchant__address span::text')

        services = self.business_details(response, category='Services')
        yellowpages_loader.add_value('services', services)
        products = self.business_details(response, category='Products and Services')
        yellowpages_loader.add_value('products', products)
        associations = self.business_details(response, category='Associations')
        yellowpages_loader.add_value('associations', associations)
        specialties = self.business_details(response, category='Specialties')
        yellowpages_loader.add_value('specialties', specialties)

        yellowpages_loader.add_css('average_rating', 'span.merchant__rating')
        yellowpages_loader.add_css('review_content', 'p.review-content_text')

        yellowpages_loader.add_css('website', 'li.mlr__item--website ul li a span.mlr__sub-text::text')

        if self.website(response):
            yellowpages_loader.add_value('website', response.urljoin(self.website(response)))

        yellowpages_loader.add_value('search_category', response.meta['search_category'])

        return yellowpages_loader.load_item()

    def business_details(self, response, category):
        raw_businessdetails = response.css('div#businessSection .business__details').extract()
        business_titles = response.css('div#businessSection .business__details h2::text').extract()
        for business in raw_businessdetails:
            for title in business_titles:
                if set(category) == set(self.clean_space(title)) and category in business:
                    return business

    def clean_space(self, value):
        return value.strip("\n")

    def website(self, response):
        return response.css('li.mlr__item--website a.mlr__item__cta::attr(href)').extract_first()

