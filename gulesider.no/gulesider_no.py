import os
import re
import csv
import urllib.parse

from scrapy.http import Request
from scrapy.spiders import CrawlSpider
from scrapylab.items import GuleSiderItemLoader


class GuleSider(CrawlSpider):
    name = 'gulesider'
    allowed_domains = ['gulesider.no']
    start_urls = ['https://www.gulesider.no']
    start_urls_t = 'https://www.gulesider.no/finn:{}'
    review_urls_t = 'https://www.gulesider.no/query?what=yp_review&eco_id={}'
    categories = []

    def __init__(self):
        super(GuleSider).__init__()
        self.categories = self.read_file(
            # urllib.parse.urljoin('{}{}'.format(os.getcwd(), '/'), 'search-data/Categories_Generic.csv')
            urllib.parse.urljoin('{}{}'.format(os.getcwd(), '/'), 'search-data/Categories_Generic_test.csv')
        )

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

    def parse(self, response):
        for category in self.categories:
            url = self.start_urls_t.format(category)
            request = Request(response.urljoin(url), callback=self.parse_urls)
            request.meta['search_category'] = category
            yield request

    def parse_urls(self, response):
        yield self.pagination(response)
        product_urls = response.css('.hit-company-name-ellipsis a::attr(href)').extract()
        for url in product_urls:
            request = Request(response.urljoin(url), callback=self.parse_item)
            request.meta['search_category'] = response.meta.get('search_category')
            yield request

    def pagination(self, response):
        next_url = response.css('.page-next a::attr(href)').extract_first()
        request = Request(response.urljoin(next_url), callback=self.parse_urls)
        request.meta['search_category'] = response.meta.get('search_category')
        return request

    def parse_item(self, response):
        loader = GuleSiderItemLoader(response=response)

        loader.add_value('search_category', response.meta.get('search_category'))
        loader.add_value('url', response.url)
        loader.add_css('company_name', '.ip-company-name::text')
        loader.add_css('telephone', '.tel::attr(data-phone)')
        loader.add_css('address', '.address-wrap span::text')
        loader.add_css('postcode', '.postal-code::text'),
        loader.add_css('city', '.locality::text')
        loader.add_css('website', '.homepage a::text')
        loader.add_css('categories', '.addax-cs_ip_categories_click::text')
        loader.add_css('certifications', '.certification-list li img::attr(title)')
        # loader.add_value('email', item_detail.get('email'))

        about_us = response.css('.e-product::text').extract()
        about_us = about_us + (response.css('.markup_text::text').extract())
        loader.add_value('about_us', about_us)
        # loader.add_value('services', self.extract_business(item_businesses, ['Diensten']))
        # loader.add_value('products', self.extract_business(item_businesses, ['Producten']))

        no_of_rev = response.css('.ip-has-reviews::Text').extract_first()
        if no_of_rev:
            loader.add_css('average_rating', '.hidden.rating::text')
            loader.add_value('number_of_reviews', no_of_rev)
            item = loader.load_item()

            eco_id = re.findall(':(\d+)', response.url)
            rev_url = self.review_urls_t.format(eco_id[0])
            request = Request(response.urljoin(rev_url), callback=self.parse_review, meta={'item': item})

            yield request
        else:
            yield loader.load_item()

    def parse_review(self, response):
        item = response.meta.get('item')
        raw_reviews = response.css('.reviews-review-text::text').extract()
        item['review_content'] = ' | '.join([r.strip() for r in raw_reviews if len(r.strip())])
        yield item


