# -*- coding: utf-8 -*-
from urlparse import urlparse, urljoin

from scrapy.http import Request
from urlparse import urljoin, urlparse, parse_qs
from scrapinghub.spider import BaseSpider
from documents_download.items import DocumentsDownloadItem
import re


class LexeuropaspiderSpider(BaseSpider):
    name = "LexEuropaSpider"
    allowed_domains = ["europa.eu"]
    start_urls = (
        'http://eur-lex.europa.eu/browse/institutions/council.html',
    )

    category_urls = []
    search_years = []

    def parse(self, response):
        for url in response.xpath('.//*[contains(@id,"arrow") and not(contains(.,"Positions"))]/@href').extract():
            self.category_urls.append(self.convert_into_absolute_url(url))
        return self.get_next_request()

    def get_documents(self, response):
        query_string = urlparse(response.url).query
        year = parse_qs(query_string)['DD_YEAR'][0] if parse_qs(query_string).get('DD_YEAR') else ''
        browse_by = parse_qs(query_string)['name'][0].split('by:', 1)[1] if parse_qs(query_string).get('name') else ''
        search_terms = '%s/%s' % (browse_by, year)
        for url in response.xpath('.//a[*[text()="pdf"]]/@href').extract():
            complete_url = self.convert_into_absolute_url(url)
            item = DocumentsDownloadItem()
            file_name_match = re.search('([^:]+)&', url)
            if file_name_match:
                item['file_name'] = file_name_match.group(1)
            item['file_location'] = search_terms
            item['file_url'] = complete_url
            yield item

        # for next_page
        if response.xpath('(.//span[@class="currentPage"])[1]/following-sibling::a[1]'):
            next_page_url = self.get_text_from_node(response.xpath('(.//span[@class="currentPage"])[1]/following-sibling::a[1]/@href'))
            yield Request(self.convert_into_absolute_url(next_page_url), callback=self.get_documents)
        yield  self.get_next_request()


    def get_next_request(self):
        if self.search_years:
            return Request(self.search_years.pop(0), callback=self.get_documents)
        if self.category_urls:
            return Request(self.category_urls.pop(0), callback=self.get_years)

    def get_years(self, response):
        years = response.xpath('.//*[@class="leaf"]')
        for year in years:
            year_text = year.xpath('./text()').extract()[0].strip()
            if year_text != 'Other' and int(year_text) > 1979:
                url = self.convert_into_absolute_url(year.xpath('./a/@href').extract()[0])
                self.search_years.append(url)
        return self.get_next_request()

    def convert_into_absolute_url(self, url):
        parsed_url = urlparse(url.strip('./').strip('../'))
        if not parsed_url.scheme:
            return urljoin('http://eur-lex.europa.eu/', url.strip('./').strip('../'))
        return url

