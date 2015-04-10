# -*- coding: utf-8 -*-
from urlparse import urlparse, urljoin

from scrapy.http import Request
from scrapy.spider import Spider

from documents_download.items import DocumentsDownloadItem


class LexeuropaspiderSpider(Spider):
    name = "LexEuropaSpider"
    allowed_domains = ["europa.eu"]
    start_urls = (
        'http://eur-lex.europa.eu/browse/institutions/council.html',
    )

    category_urls = []
    search_years = []
	
    def parse(self, response):
        # get only one category extract()[0:1]:
        for url in response.xpath('.//*[contains(@id,"arrow") and not(contains(.,"Positions"))]/@href').extract():
            self.category_urls.append(self.convert_into_absolute_url(url))
        return self.get_next_request()

    def get_documents(self, response):
        search_terms = response.url.split('by:', 1)[1].split('&')[0] + '/' + \
                       response.url.split('YEAR=', 1)[1].split('&')[0]
        for url in response.xpath('.//a[*[text()="pdf"]]/@href').extract():
            complete_url = self.convert_into_absolute_url(url)
            item = DocumentsDownloadItem()
            item['file_name'] = complete_url.split('X:')[1].split('&')[0]
            item['file_location'] = search_terms
            item['file_url'] = complete_url
            yield item

        # for next_page
        total = response.xpath('.//*[@name="WT.oss_r"]/@content').extract()
        if total:
            pages = int(total[0]) / 10 + (int(total[0]) % 10 != 0)
            for i in range(2, pages + 1):
                url = response.url + '&page=%s' % i
                yield Request(self.convert_into_absolute_url(url), callback=self.get_documents)
        yield self.get_next_request()

    def get_next_request(self):
        if self.search_years:
            return Request(self.search_years.pop(0), callback=self.get_documents)
        if self.category_urls:
            return Request(self.category_urls.pop(0), callback=self.get_years)

    def get_years(self, response):
        years = response.xpath('.//*[@class="leaf"]')
        # get only one year years[0:1]
        for year in years:
            year_text = year.xpath('./text()').extract()[0].strip()
            if year_text != 'Other' and int(year_text) > 1980:
                url = self.convert_into_absolute_url(year.xpath('./a/@href').extract()[0])
                self.search_years.append(url)
        return self.get_next_request()

    def convert_into_absolute_url(self, url):
        parsed_url = urlparse(url.strip('./').strip('../'))
        if not parsed_url.scheme:
            return urljoin('http://eur-lex.europa.eu/', url.strip('./').strip('../'))
        return url

