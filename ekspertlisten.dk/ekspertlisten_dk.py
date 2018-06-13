import os
import csv
import json
import urllib.parse

from statistics import mean
from scrapy.http import Request
from urllib.parse import urlencode
from scrapy.spiders import CrawlSpider
from scrapylab.items import EkspertListenItemLoader


class EkspertListen(CrawlSpider):
    name = 'ekspertlisten'
    allowed_domains = ['ekspertlisten.dk']
    start_urls = ['https://www.ekspertlisten.dk/find']
    # start_urls = ['https://www.ekspertlisten.dk']
    start_urls_t = 'https://www.ekspertlisten.dk/find/{}'
    categories = []

    def __init__(self):
        super(EkspertListen).__init__()
        self.categories = self.read_file(
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
        cat_xpath = '//*[contains(@for, "industry")]/a/{}'
        category_urls = response.xpath(cat_xpath.format('@href')).extract()
        category_text = response.xpath(cat_xpath.format('text()')).extract()

        category_dict = dict(zip(category_urls, category_text))

        for url, url_text in category_dict.items():
            if url != '/find':
                request = Request(response.urljoin(url), callback=self.parse_urls)
                request.meta['search_category'] = url_text
                yield request

        # for category in self.categories:
        #     params = {
        #         "q": category
        #     }
        #     url = self.start_urls_t.format(urlencode(params))
        #     request = Request(response.urljoin(url), callback=self.parse_urls)
        #     request.meta['search_category'] = category
        #     yield request

    def parse_urls(self, response):
        yield self.pagination(response)
        product_urls = response.css('.item-name a::attr(href)').extract()
        for url in product_urls:
            request = Request(response.urljoin(url), callback=self.parse_item)
            request.meta['search_category'] = response.meta.get('search_category')
            yield request

    def pagination(self, response):
        next_url = response.xpath('//*[@aria-label="Next"]//@href').extract_first()
        request = Request(response.urljoin(next_url), callback=self.parse_urls)
        # request = Request(response.urljoin(next_url), callback=self.parse)
        request.meta['search_category'] = response.meta.get('search_category')
        return request

    def parse_item(self, response):
        loader = EkspertListenItemLoader(response=response)
        loader.add_value('search_category', response.meta.get('search_category'))
        loader.add_value('url', response.url)
        loader.add_css('company_name', '.title-text h1::text')
        loader.add_css('categories', '.title-text h3::text')

        xpath = '//*[@class="companyinfo"]//li[span/text()="{0}"]{1}'
        loader.add_xpath('telephone', xpath.format('Telefon:', '/text()'))
        loader.add_xpath('address', xpath.format('Adresse:', '/text()'))
        loader.add_xpath('website', xpath.format('Web:', "/a/text()"))
        loader.add_css('about_us', '#profile p::text')

        postcode = response.xpath('//*[@class="tile"][contains(h3/text(), "Lignende firmaer")]/a/@href').extract_first()
        loader.add_value('postcode', postcode.split("/").pop()),

        rating = response.css('.rating-score::attr(class)').re('rating-score-(\d)')
        rating = list(map(int, rating))
        if rating:
            loader.add_value('average_rating', str(mean(rating)))
            loader.add_value('number_of_reviews', str(len(rating)))
            loader.add_css('review_content', '.rating-body p::text')

        return loader.load_item()
