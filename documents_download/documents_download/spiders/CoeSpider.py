from urlparse import urljoin, urlparse, parse_qs

from scrapy import log

from scrapy.http import Request, FormRequest
from scrapy.spider import Spider

from documents_download.items import DocumentsDownloadItem


class CoeSpider(Spider):
    name = 'coe_spider'
    start_urls = [
        'http://www.coe.int/T/CM/System/WCDsearch.asp?ShowRes=yes&DocType=docDecision&FilingPlan=fplCM_VolDecisions'
        '&Language=lanEnglish&Sector=secCM&ShowCrit=top&ShowPeriodBox=dates'
        '&ShowPaginationBox=no&ShowFullTextSearch=yes&ShowDocTypeBox=no&ShowEntityBox=no&ShowEventBox=no'
        '&ShowGeoBox=no&ShowLanguageBox=no%20&ShowThemeBox=no&ShowSectorBox=no&ShowSectorLevelBox=no'
        '&ShowFileRefBox=no&ShowKeywordBox=no&ResultTitle=Compilation%20of%20decisions%20by%20meeting&'
        'CritTitle=Compilation%20of%20decisions%20by%20meeting'
    ]

    base_url = 'https://wcd.coe.int'

    def parse(self, response):
        frame_url = response.xpath(".//*[@id='wcdFrame']//@src").extract()[0]
        return Request(url=frame_url,
                       callback=self.parse_frame_data)

    def parse_frame_data(self, response):
        doc_links = response.xpath("//td[@class='paddingLR25px']//a//@href").extract()
        for link in doc_links:
            url = urljoin(self.base_url, link)
            yield Request(url=url,
                          callback=self.parse_download_link)

        next_page_number = int(response.xpath("//*[@class='WCDPagination_NumCourant']//text()").extract()[0]) + 1
        if response.xpath(".//a[contains(.,'Next')]"):
            data = {'PageNumber': str(next_page_number)}
            yield FormRequest.from_response(response,
                                            formname='wcdFormRes',
                                            formdata=data,
                                            callback=self.parse_frame_data)

    def parse_download_link(self, response):
        download_link = ''
        word_file_link = response.xpath(".//*[@class='WCDBar_docBarButton'][contains(text(),'WORD')]//@href").extract()
        if word_file_link:
            download_link = urljoin(self.base_url, word_file_link[0])
        else:  # file may be in PDF format
            pdf_file_link = response.xpath(
                ".//*[@class='WCDBar_docBarButton'][contains(text(),'PDF')]//@href").extract()
            if pdf_file_link:
                download_link = urljoin(self.base_url, pdf_file_link[0])
        if download_link:
            item = DocumentsDownloadItem()
            item['file_url'] = download_link
            item['file_name'] = self.get_title(download_link)  # item ID will be the file name
            return item
        else:
            self.log("File does not exist in WORD or PDF format", level=log.WARNING)

    def get_title(self, url):
        query_string = urlparse(url).query
        if query_string:
            doc_id = parse_qs(query_string)['DocId'][0]
            return doc_id
