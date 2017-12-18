import time
from concurrent import futures
from queue import Queue
from threading import Lock
import requests
from lxml import html


class WebCrawlerConcurrent:
    def __init__(self, download_delay, max_request_count, concurrent_request_count):
        self.download_delay = download_delay
        self.max_request_count = max_request_count
        self.request_pool_count = concurrent_request_count
        self.loop = None
        self.executor = futures.ThreadPoolExecutor(max_workers=self.request_pool_count)
        self.request_count = 0
        self.total_bytes_downloaded = 0
        self.last_request_time = None
        self.visited_url = []
        self.crawlable_url = Queue()
        self.items = []
        self.futures = []
        self.bytes_lock = Lock()

    def crawl(self, url):
        self.last_request_time = time.time()
        self.crawlable_url.put_nowait(url)
        self.executor.submit(self.schedule_tasks())
        self.executor.shutdown(True)

    def schedule_tasks(self):
        while True:
            while not self.crawlable_url.empty():
                url = self.crawlable_url.get_nowait()
                if self.max_request_count > self.request_count:
                    self.futures.append(self.executor.submit(self._crawl, url))
                    self.bytes_lock.acquire()
                    try:
                        self.request_count += 1
                    finally:
                        self.bytes_lock.release()
            pending = [task for task in self.futures if not task.done()]
            if len(pending) == 0:
                return
            else:
                time.sleep(1)

    def _crawl(self, crawlable_url):
        if 0 == len([url for url in self.visited_url if crawlable_url == url]):
            self.visited_url.append(crawlable_url)
            current_time = time.time()

            if current_time - self.last_request_time < self.download_delay:
                time.sleep(current_time - self.last_request_time)

            current_time = time.time()
            source = requests.get(crawlable_url)

            self.bytes_lock.acquire()
            try:
                self.last_request_time = current_time
                self.total_bytes_downloaded += len(source.content)
            finally:
                self.bytes_lock.release()

            source_element = html.fromstring(source.content)
            pages = source_element.xpath(
                "//div[contains(@class, 'paginationContainer')]//a[contains(@class, 'phm')]/@href")
            for page in pages:
                self.crawlable_url.put(page)

            forward_links_xpath = "//div[@id='resultsColumn']//ul[contains(@class,'mvn')]/li[contains(@class,'xsCol12Landscape')]//a[@class='tileLink']/@href"
            forward_links = source_element.xpath(forward_links_xpath)
            for link in forward_links:
                self.crawlable_url.put("https://www.trulia.com" + link)

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
