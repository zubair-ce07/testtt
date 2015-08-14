# -*- coding: utf-8 -*

from scrapy.spider import Spider
import re
from documents_download.items import DocumentsDownloadItem


class EuropaeuspiderSpider(Spider):
    name = "EuropaEuSpider"
    allowed_domains = ["europa.eu"]
    list_of_files = []
    start_urls = []

    def start_requests(self):
        for year in range(1999, 2015):
            url = 'http://register.consilium.europa.eu/content/out?PUB_DOC=>0&RESULTSET=1&DOC_SUBJECT_PRIM=PUBLIC&lang=EN&i=ACT&ROWSPP=25&ORDERBY=DOC_DATE DESC&DOC_LANCD=EN&typ=SET&NRROWS=500&DOC_TITLE=%s' % year
            yield self.make_requests_from_url(url)

    def parse(self, response):
        folder_title = response.url.split('DOC_TITLE=')[1]
        all_urls = response.xpath(".//a[img[contains(@src,'pdf')]]/@href").extract()
        for url in all_urls:
            item = DocumentsDownloadItem()
            file_name = re.search('document/(.*)/en',url).group(1)
            item['file_url'] = url
            item['file_name'] = file_name
            item['file_location'] = folder_title
            yield item
