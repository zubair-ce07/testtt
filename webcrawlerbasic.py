from lxml import html
import requests
import time


class WebCrawlerBasic:
    def __init__(self, download_delay, max_request_count, concurrent_request_count):
        self.download_delay = download_delay
        self.max_request_count = max_request_count
        self.pending_crawls = []
        self.loop = None
        self.threads = 1
        self.request_count = 0
        self.total_bytes_downloaded = 0
        self.last_request_time = None
        self.visited_url = []
        self.crawlable_url = []
        self.items = []

    def crawl(self, url):
        self.crawlable_url.append(url)
        self.crawl_page()

    def crawl_page(self):
        while len(self.crawlable_url) > 0:
            url = self.crawlable_url.pop(0)
            self.crawl_element(url)

    def crawl_element(self, crawlable_url):
            if 0 == len([url for url in self.visited_url if crawlable_url == url]) and self.request_count < self.max_request_count:
                self.last_request_time = time.time()
                self.request_count += 1
                source = requests.get(crawlable_url)
                self.visited_url.append(crawlable_url)
                self.total_bytes_downloaded += len(source.content)
                source_element = html.fromstring(source.content)
                pages = source_element.xpath("//div[contains(@class, 'paginationContainer')]//a[contains(@class, 'phm')]/@href")
                for page in pages:
                    if 0 == len([url for url in self.crawlable_url if page == url]):
                        self.crawlable_url.append(page)

                forward_links_xpath = "//div[@id='resultsColumn']//ul[contains(@class,'mvn')]/li[contains(@class,'xsCol12Landscape')]//a[@class='tileLink']/@href"
                forward_links = source_element.xpath(forward_links_xpath)
                for link in forward_links:
                    if 0 == len([url for url in self.crawlable_url if link == url]):
                        self.crawlable_url.append("https://www.trulia.com"+link)

                property_details_xpath = "//div[@id='propertyDetails']"
                property_details = source_element.xpath(property_details_xpath)
                for detail in property_details:
                   item = []
                   heading_xpath = ".//span[contains(@class,'headingDoubleSuper')]/text()"
                   item += detail.xpath(heading_xpath)
                   address_xpath = ".//span[contains(@class,'headlineDoubleSub')]/span/text()|/a/text()"
                   address = ' '.join(detail.xpath(address_xpath))
                   item.append(address)
                   details_xpath = ".//ul[contains(@class,'listingDetails')]/li/text()"
                   property_detail = ' '.join(detail.xpath(details_xpath))
                   item.append(property_detail)
                   # print()
                   # for attribute in item:
                   #     print(attribute)
                   # print()
                   self.items.append(item)





