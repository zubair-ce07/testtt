from threading import Lock
from queue import Queue
import requests
import asyncio
import time

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
            self.extract_property_details(crawlable_url, source_element)

    def extract_pagination_links(self, source_element):
        pages = source_element.xpath(
            "//div[contains(@class, 'paginationContainer')]//a[contains(@class, 'phm')]/@href")
        for page in pages:
            self.crawlable_url.put(page)

    def extract_detail_links(self, source_element):
        forward_links_xpath = "//ul[contains(@class,'row')]//a[@class='tileLink']/@href"
        forward_links = source_element.xpath(forward_links_xpath)
        for link in forward_links:
            self.crawlable_url.put("https://www.trulia.com" + link)

    def extract_property_details(self, url, source_element):
        property_details_xpath = "//div[@id='propertyDetails']"
        property_details = source_element.xpath(property_details_xpath)
        if property_details:
            print(f"Current_Url {url}")
        for detail in property_details:
            item = {}
            heading_xpath = ".//span[contains(@class,'headingDoubleSuper')]/text()"
            item.update({"name": detail.xpath(heading_xpath)})
            address_xpath = ".//span[contains(@class,'headlineDoubleSub')]/span/text()|/a/text()"
            address = {'address': ' '.join(detail.xpath(address_xpath))}
            item.update(address)
            details_xpath = ".//ul[contains(@class,'listingDetails')]/li/text()"
            details = ' '.join(detail.xpath(details_xpath))
            property_detail = {'property_details': details}
            item.update(property_detail)
            print()
            for attribute in item.values():
                print(attribute)
            print()
            self.items.append(item)
