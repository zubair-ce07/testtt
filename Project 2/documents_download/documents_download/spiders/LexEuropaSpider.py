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
            self.category_urls.append(urljoin(response.url, url))
        return self.get_next_request()

    def get_documents(self, response):
        query_string = urlparse(response.url).query
        year = parse_qs(query_string)['DD_YEAR'][0] if parse_qs(query_string).get('DD_YEAR') else ''
        browse_by = parse_qs(query_string)['name'][0].split('by:', 1)[1] if parse_qs(query_string).get('name') else ''
        search_terms = '%s/%s' % (browse_by, year)
        for url in response.xpath('.//a[*[text()="pdf"]]/@href').extract():
            complete_url = urljoin(response.url, url)
            item = DocumentsDownloadItem()
            file_name_match = re.search('([^:]+)&', url)
            if file_name_match:
                item['file_name'] = file_name_match.group(1)
            item['file_location'] = search_terms
            item['file_url'] = complete_url
            yield Request(complete_url, method="head",callback=self.parse_documents, meta={'item': item})

        # for next_page
        if response.xpath('(.//span[@class="currentPage"])[1]/following-sibling::a[1]'):
            next_page_url = self.get_text_from_node(response.xpath('(.//span[@class="currentPage"])[1]/following-sibling::a[1]/@href'))
            yield Request(urljoin(response.url, next_page_url), callback=self.get_documents)
        yield self.get_next_request()

    def parse_documents(self,response):
        item = response.meta['item']
        if 'html' in response.headers['Content-Type']:
            yield Request(response.url, dont_filter=True, callback=self.parse_sub_documents, meta={'item': item})
        else:
            yield item
        yield self.get_next_request()

    def parse_sub_documents(self, response):
        parent = response.meta['item']
        file_location = '%s/%s' % (parent['file_location'],parent['file_name'])
        for url in response.xpath('.//*[@class="buttonLike buttonLink"]/following-sibling::ul[1]/li/a/@href').extract():
            item = DocumentsDownloadItem()
            file_name = re.search('cellar\s*:\s*([^&]+)', url).group(1).replace('/','_')
            item['file_url'] = urljoin(response.url,url)
            item['file_location'] = file_location
            item['file_name'] = file_name
            yield item
        yield self.get_next_request()

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
                url = urljoin(response.url, year.xpath('./a/@href').extract()[0])
                self.search_years.append(url)
        return self.get_next_request()
