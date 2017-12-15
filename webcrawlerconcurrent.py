import time
import asyncio
from concurrent import futures
import multiprocessing
from lxml import html
import requests
from elements.webpage import WebPage
from elements.element import Element
from data.datanode import DataNode


class WebCrawlerConcurrent:
    def __init__(self, download_delay, max_request_count, concurrent_request_count):
        self.download_delay = download_delay
        self.max_request_count = max_request_count
        self.request_pool_count = concurrent_request_count
        self.executor = None
        self.threads = 1
        self.request_count = 0
        self.last_request_time = None
        self.total_bytes_downloaded = 0
        self.visited_url = []

    def crawl(self, web_page: WebPage):
        self.executor = futures.ThreadPoolExecutor(max_workers=self.request_pool_count)
        url = web_page.url_string("")
        self.last_request_time = time.time()
        self.visited_url.append(url)
        source = requests.get(url)
        self.request_count += 1
        doc = html.fromstring(source.content) 
        self.total_bytes_downloaded += len(source.content)
        result = self._crawl_element([doc], web_page)
        return result

    def _crawl_element(self, source_elements, element: Element):
        items = []
        for source in source_elements:
            item = DataNode(element.multiple)
            item.name = element.item_name()
            item.add_data_items(self._parse_data(source, element))
            if (len(element.crawlable_links) > 0):
                self.executor.submit(self._crawl_sub_pages(item, source, element))

            for sub_element in element.data_elements:
                sub_source = source.xpath(sub_element.xpath())
                if len(sub_source) > 0:
                    sub_items = self._crawl_element(sub_source, sub_element)
                    item.add_sub_items(sub_items)
            items.append(item)
        return items

    def _parse_data(self, source_element, element: Element):
        data = {}
        for leaf in element.leaf_elements:
            text = source_element.xpath(leaf.xpath())
            if len(text) == 0:
                data.update({leaf.name: None})
            elif len(text) == 1:
                data.update({leaf.name: text[0]})
            else:
                data.update({leaf.name: text})
        return data

    def _crawl_sub_pages(self, item, source_element, element):
        list = []
        thread_number = self.threads
        self.threads += 1
        for crawlable in element.crawlable_links:
            if self.max_request_count > self.request_count:
                matches = source_element.xpath(crawlable.xpath())
                for match in matches:
                    url = crawlable.url_string(match.attrib.get('href'))
                    visited_url = [explored_url for explored_url in self.visited_url if explored_url == url]
                    if len(visited_url) == 0:
                        self.visited_url.append(url)
                        self.request_count += 1
                        current_time = time.time()

                        if current_time - self.last_request_time < self.download_delay:
                            time.sleep(current_time - self.last_request_time)
                            current_time = time.time()

                        self.last_request_time = current_time

                        response = requests.get(url)

                        self.total_bytes_downloaded += len(response.content)
                        doc = html.fromstring(response.content)
                        crawled_list = self._crawl_element(doc, crawlable)
                        list = list + crawled_list
        item.add_sub_items(list)
