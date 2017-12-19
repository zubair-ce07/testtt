import asyncio
import time
from queue import Queue
from threading import Lock

import requests
from lxml import html


class Spider:
    def __init__(self, download_delay):
        self.loop = asyncio.new_event_loop()
        self.download_delay = download_delay
        self.total_bytes_downloaded = 0
        self.last_request_time = None
        self.crawlable_url = Queue()
        self.items = []
        self.visited_url = []
        self.bytes_lock = Lock()

    def crawl(self, crawlable_url):
        visited = [url for url in self.visited_url if crawlable_url == url]
        if not visited:
            self.last_request_time = time.time()
            self.visited_url.append(crawlable_url)

            current_time = time.time()

            if current_time - self.last_request_time < self.download_delay:
                asyncio.sleep(current_time - self.last_request_time)

            self.last_request_time = current_time

            source = requests.get(crawlable_url)

            self.total_bytes_downloaded += len(source.content)
            source_element = html.fromstring(source.content)

            self.extract_pagination_links(source_element)
            self.extract_detail_links(source_element)
            self.extract_property_details(source_element)

    def extract_pagination_links(self, source_element):
        pages = source_element.xpath(
            "//div[contains(@class, 'paginationContainer')]//a[contains(@class, 'phm')]/@href")
        for page in pages:
            self.crawlable_url.put(page)

    def extract_detail_links(self, source_element):
        forward_links_xpath = "//div[@id='resultsColumn']//ul[contains(@class,'mvn')]/li[contains(@class,'xsCol12Landscape')]//a[@class='tileLink']/@href"
        forward_links = source_element.xpath(forward_links_xpath)
        for link in forward_links:
            self.crawlable_url.put("https://www.trulia.com" + link)

    def extract_property_details(self, source_element):
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
