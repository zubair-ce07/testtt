# -*- coding: utf-8 -*

from scrapy.spider import Spider

from documents_download.items import DocumentsDownloadItem


class EuropaeuspiderSpider(Spider):
    name = "EuropaEuSpider"
    allowed_domains = ["europa.eu"]
    list_of_files = []
    start_urls = []

    def __init__(self, **kwargs):
        for year in range(1999, 2015):
            url = 'http://register.consilium.europa.eu/content/out?PUB_DOC=>0&RESULTSET=1&DOC_SUBJECT_PRIM=PUBLIC&lang=EN&i=ACT&ROWSPP=25&ORDERBY=DOC_DATE DESC&DOC_LANCD=EN&typ=SET&NRROWS=500&DOC_TITLE=%s' % year
            self.start_urls.append(url)
        super(EuropaeuspiderSpider, self).__init__(**kwargs)

    def parse(self, response):
        folder_title = response.url.split('DOC_TITLE=')[1]
        all_names = response.xpath(".//*[contains(@id,'IMG_AREA')]/@onclick").extract()
        for name in all_names:
            item = DocumentsDownloadItem()
            file_name = name.split(",'")[1].split("'")[0]
            item['file_url'] = 'http://data.consilium.europa.eu/doc/document/%s/en/pdf' % file_name
            item['file_name'] = file_name
            item['file_location'] = folder_title
            yield item
