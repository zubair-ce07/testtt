from urlparse import urljoin, urlparse, parse_qs

from scrapy import log
from scrapinghub.spider import BaseSpider

from scrapy.http import Request, FormRequest
from scrapy.spider import Spider

from documents_download.items import DocumentsDownloadItem


class CoeSpider(BaseSpider):
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
        for link in response.xpath("//td[@class='paddingLR25px']//a"):
            url = urljoin(self.base_url, self.get_text_from_node(link.xpath('.//@href')))
            name = self.get_text_from_node(link.xpath('.//text()'))
            yield Request(url=url,
                          callback=self.parse_download_link, meta={'name': name})

        next_page_number = int(response.xpath("//*[@class='WCDPagination_NumCourant']//text()").extract()[0]) + 1
        if response.xpath(".//a[contains(.,'Next')]"):
            data = {'PageNumber': str(next_page_number)}
            yield FormRequest.from_response(response,
                                            formname='wcdFormRes',
                                            formdata=data,
                                            callback=self.parse_frame_data)

    def parse_download_link(self, response):
        download_link = ''
        doc_name = response.meta['name'].replace('/', '_')
        word_file_link = response.xpath(".//*[@class='WCDBar_docBarButton'][contains(text(),'WORD')]//@href").extract()
        if word_file_link:
            download_link = urljoin(self.base_url, word_file_link[0])
        elif response.xpath(".//*[@class='WCDBar_docBarButton'][contains(text(),'PDF')]"):  # file may be in PDF format
            pdf_file_link = response.xpath(
                ".//*[@class='WCDBar_docBarButton'][contains(text(),'PDF')]//@href").extract()
            if pdf_file_link:
                download_link = urljoin(self.base_url, pdf_file_link[0])
        elif response.xpath(".//*[@class='WCDBar_docBarButton'][contains(text(),'DOWNLOAD')]"):
            if response.xpath('.//*[@class="WCDRend_PrintablePaper"]/*[@class="WCDRend_link"]'):
                for link in response.xpath('.//*[@class="WCDRend_PrintablePaper"]/*[@class="WCDRend_link"]//li/a'):
                    download_link = urljoin(self.base_url, self.get_text_from_node(link.xpath('./@href')))
                    item = DocumentsDownloadItem()
                    item['file_url'] = download_link
                    item['file_name'] = '%s_%s' % (doc_name,
                                                   self.get_text_from_node(link.xpath('./text()')).replace('.pdf',
                                                                                                           ''))  # item ID will be the file name
                    item['file_location'] = doc_name
                    yield item
            else:
                for link in response.xpath('.//*[@id="SMenuImprimable"]//td/a'):
                    download_link = urljoin(self.base_url, self.get_text_from_node(link.xpath('./@href')))
                    item = DocumentsDownloadItem()
                    item['file_url'] = download_link
                    item['file_name'] = '%s_%s_%s' % (
                    doc_name, self.get_text_from_node(link.xpath('./text()')), self.document_id(download_link))
                    item['file_location'] = doc_name  # item ID will be the file name
                    yield item

        else:
            self.log("File does not exist in WORD or PDF format", level=log.WARNING)
        if download_link:
            item = DocumentsDownloadItem()
            item['file_url'] = download_link
            item['file_name'] = doc_name  # item ID will be the file name
            yield item

    def document_id(self, url):
        query_string = urlparse(url).query
        if query_string:
            doc_id = parse_qs(query_string)['DocId'][0]
            return doc_id

