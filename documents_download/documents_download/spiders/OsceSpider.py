from urlparse import urljoin, urlparse

from scrapy.http import FormRequest, Request
from scrapy.spider import Spider

from documents_download.items import DocumentsDownloadItem


class OsceSpider(Spider):
    name = 'osce_spider'
    start_urls = ["http://www.osce.org/resources/documents"]

    base_url = "http://www.osce.org"  # 'To append with relative download url.
    page_to_crawl = 1

    def parse(self, response):
        data = {"filters_1": '15',
                "date_from": '1994',
                "document_type": '462',
                'language': 'en',
                'op': 'Apply Filters',
                'solrsort_field': 'score',
                'solrsort_order': 'desc',
                'rows': '10',
                'filters_2': '0',
                'filters_3': '0',
                'filters_4': '0',
                'date_to': '',
                'form_build_id': 'form-b8269dd21d4683ff29b6cb35f1ada469',
                'form_id': 'osce_search_form_resources'
        }
        url = urljoin(self.base_url, "/resources/documents")
        yield FormRequest(url=url,
                          formdata=data,
                          callback=self.parse_listing)

    def parse_listing(self, response):
        doc_download_links = response.xpath("//ul[@class='links']//a[contains(text(),'English')]//@href").extract()
        for link in doc_download_links:
            full_link = urljoin(self.base_url, link)
            item = DocumentsDownloadItem()
            item['file_url'] = full_link
            item['file_name'] = self.get_title(full_link)  # item ID will be the file name
            item['page'] = self.page_to_crawl
            yield item

        next_page_url = response.xpath("//li[contains(@class,'pager-current')]/following-sibling::li[1]//a//@href").extract()
        if next_page_url:
            next_page_full_url = urljoin(self.base_url, next_page_url[0])
            yield Request(url=next_page_full_url,
                          callback=self.parse_listing)
            self.page_to_crawl += 1

    def get_title(self, url):
        query_path = urlparse(url).path
        if query_path:
            parts = query_path.split('/')  # example /pc/12323
            if len(parts) == 3:
                doc_id = parts[2]
            else:
                doc_id = parts[1]
            return doc_id




