from urlparse import urljoin, urlparse

from scrapy.http import FormRequest, Request
from scrapy.spider import Spider
import re

from documents_download.items import DocumentsDownloadItem
from scrapinghub.spider import BaseSpider

class OsceSpider(BaseSpider):
    name = 'osce_spider'
    start_urls = ["http://www.osce.org/resources/documents"]

    base_url = "http://www.osce.org"  # 'To append with relative download url.
    page_to_crawl = 1

    def parse(self, response):
        return Request('http://www.osce.org/resources/documents/?filters=+im_taxonomy_vid_1:%2815%29+im_taxonomy_vid_22:%28462%29+sm_translations:%28en%29&solrsort=score%20desc&rows=10', callback=self.parse_listing)

    def parse_listing(self, response):
        for link in response.xpath("//ul[@class='links']//a[contains(text(),'English')]"):
            full_link = urljoin(self.base_url, self.get_text_from_node(link.xpath('.//@href')))
            item = DocumentsDownloadItem()
            item['file_url'] = full_link
            item['file_location'] = self.page_to_crawl
            item['file_name'] = self.get_title(full_link, link)  # item ID will be the file name
            item['file_location'] = self.page_to_crawl
            item['page'] = self.page_to_crawl
            yield item

        next_page_url = response.xpath("//li[contains(@class,'pager-current')]/following-sibling::li[1]//a//@href").extract()
        if next_page_url:
            next_page_full_url = urljoin(self.base_url, next_page_url[0])
            yield Request(url=next_page_full_url,
                          callback=self.parse_listing)
            self.page_to_crawl += 1

    def get_title(self, url, response, ):
        match_title = re.search('(\w+)\?', url)
        title_id = match_title.group(1)
        title = self.get_text_from_node(response.xpath('.//@title'))
        return '%s_%s' % (title.replace('/', '_')[:200], title_id)



